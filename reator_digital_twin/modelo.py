"""Modelo físico, controle (MPC de rastreamento e Economic MPC), detecção de falha e
camada de proteção independente (SIS) para um CSTR não-isotérmico.

Todos os parâmetros de planta vêm de uma `ConfiguracaoReator` (ver config.py) — o mesmo
código serve para qualquer reator real descrito por um arquivo YAML em `configs/`.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, NonlinearConstraint

from .config import ConfiguracaoReator


class ReatorCSTR:
    def __init__(self, config: ConfiguracaoReator = None):
        self.cfg = config or ConfiguracaoReator()
        for campo in ("V", "F", "CA0", "T0", "Pre_exp_A", "Ea_R", "DeltaH", "rho", "Cp",
                      "CA_inicial", "T_inicial", "T_alvo", "T_max_seguro", "taxa_max_Tj",
                      "Tj_min", "Tj_max", "UA_nominal", "T_trip_sis", "Tj_seguranca",
                      "preco_produto", "custo_energia"):
            setattr(self, campo, getattr(self.cfg, campo))

    def calcular_cinetica(self, CA, T):
        k = self.Pre_exp_A * np.exp(-self.Ea_R / T)
        return k * CA

    def _derivadas(self, CA, T, Tj, UA, DeltaH=None):
        DeltaH = self.DeltaH if DeltaH is None else DeltaH
        CA = max(CA, 0.0)
        taxa = self.calcular_cinetica(CA, T)
        dCAdt = (self.F / self.V) * (self.CA0 - CA) - taxa
        dTdt = ((self.F / self.V) * (self.T0 - T)) + ((-DeltaH * taxa) / (self.rho * self.Cp)) + ((UA * (Tj - T)) / (self.V * self.rho * self.Cp))
        return dCAdt, dTdt

    def _dinamica_ivp(self, t, y, Tj, UA, DeltaH=None):
        return self._derivadas(y[0], y[1], Tj, UA, DeltaH)

    def _rk4_substep(self, CA, T, Tj, UA, dt, DeltaH=None):
        k1_CA, k1_T = self._derivadas(CA, T, Tj, UA, DeltaH)
        k2_CA, k2_T = self._derivadas(CA + dt / 2 * k1_CA, T + dt / 2 * k1_T, Tj, UA, DeltaH)
        k3_CA, k3_T = self._derivadas(CA + dt / 2 * k2_CA, T + dt / 2 * k2_T, Tj, UA, DeltaH)
        k4_CA, k4_T = self._derivadas(CA + dt * k3_CA, T + dt * k3_T, Tj, UA, DeltaH)
        CA_novo = CA + (dt / 6) * (k1_CA + 2 * k2_CA + 2 * k3_CA + k4_CA)
        T_novo = T + (dt / 6) * (k1_T + 2 * k2_T + 2 * k3_T + k4_T)
        return max(0.0, CA_novo), T_novo

    def _rk4_step(self, CA, T, Tj, UA, dt, n_sub=20, DeltaH=None):
        # Subdivide cada passo de controle em substeps de RK4 para manter estabilidade
        # numérica mesmo com a cinética mais rápida/exotérmica perto da ignição.
        dt_sub = dt / n_sub
        for _ in range(n_sub):
            CA, T = self._rk4_substep(CA, T, Tj, UA, dt_sub, DeltaH)
        return CA, T

    def _avancar_com_sis(self, CA, T, Tj_mpc, UA, dt, DeltaH):
        # O SIS é um logic solver de segurança dedicado, com scan rate muito mais rápido que
        # o ciclo do MPC — aqui modelado com integração adaptativa (RK45) e detecção exata do
        # instante de cruzamento do trip, em vez de amostrar a temperatura só a cada ciclo de
        # controle (o que mascararia disparos dentro de um único intervalo do MPC).
        def evento_trip(t, y, Tj, UA, DeltaH):
            return self.T_trip_sis - y[1]
        evento_trip.terminal = True
        evento_trip.direction = -1

        sol = solve_ivp(self._dinamica_ivp, [0, dt], [CA, T], args=(Tj_mpc, UA, DeltaH),
                         method='RK45', max_step=dt / 20, events=evento_trip)
        if sol.t_events[0].size == 0:
            return sol.y[0, -1], sol.y[1, -1], False

        # Trip disparado dentro deste intervalo: o restante do passo usa resfriamento máximo.
        CA_trip, T_trip = sol.y[0, -1], sol.y[1, -1]
        dt_restante = dt - sol.t[-1]
        if dt_restante <= 0:
            return CA_trip, T_trip, True
        sol2 = solve_ivp(self._dinamica_ivp, [0, dt_restante], [CA_trip, T_trip],
                          args=(self.Tj_seguranca, UA, DeltaH), method='RK45', max_step=dt / 20)
        return sol2.y[0, -1], sol2.y[1, -1], True

    def simular_runaway(self, UA_operacao, Tj=290.0, tempo_total=20, dt=0.02, DeltaH_cenario=-250000.0):
        """Análise de risco em malha aberta (HAZOP-style). Usa um calor de reação de pior
        caso (DeltaH_cenario), mais conservador que a cinética nominal usada pelo controle
        (self.DeltaH), para representar o cenário de projeto de uma análise de segurança de
        processo — a mesma lógica de considerar impurezas/reações secundárias no pior caso
        credível em vez da condição de operação normal."""
        # Integração adaptativa (RK45) em vez de Euler explícito: essencial perto do
        # runaway, onde a dinâmica fica rígida (stiff) e o passo fixo perde precisão.
        hist_tempo = np.arange(0, tempo_total, dt)

        def evento_runaway(t, y, Tj, UA, DeltaH):
            return 600.0 - y[1]
        evento_runaway.terminal = True
        evento_runaway.direction = -1

        sol = solve_ivp(self._dinamica_ivp, [0, tempo_total], [self.CA_inicial, self.T_inicial], t_eval=hist_tempo,
                         args=(Tj, UA_operacao, DeltaH_cenario), method='RK45', max_step=dt, events=evento_runaway)

        hist_T = np.full(len(hist_tempo), sol.y[1, -1])
        hist_T[:sol.t.size] = sol.y[1]
        return hist_tempo, hist_T

    def _rollout_mpc(self, acoes_Tj, CA_atual, T_atual, dt_mpc, UA):
        CA_pred, T_pred = CA_atual, T_atual
        T_hist = np.zeros(len(acoes_Tj))
        CA_hist = np.zeros(len(acoes_Tj))
        for idx, Tj_predito in enumerate(acoes_Tj):
            CA_pred, T_pred = self._rk4_step(CA_pred, T_pred, Tj_predito, UA, dt_mpc)
            T_hist[idx] = T_pred
            CA_hist[idx] = CA_pred
        return CA_pred, T_hist, CA_hist

    def _custo_mpc(self, acoes_Tj, CA_atual, T_atual, dt_mpc, UA):
        # Rastreamento de setpoint: minimiza o desvio da temperatura em relação a T_alvo.
        _, T_pred, _ = self._rollout_mpc(acoes_Tj, CA_atual, T_atual, dt_mpc, UA)
        return float(np.sum((T_pred - self.T_alvo) ** 2))

    def _custo_economico(self, acoes_Tj, CA_atual, T_atual, dt_mpc, UA):
        # Economic MPC: minimiza custo líquido (energia da jaqueta menos receita da
        # conversão), em vez de perseguir um setpoint de temperatura fixo e arbitrário.
        _, T_hist, CA_hist = self._rollout_mpc(acoes_Tj, CA_atual, T_atual, dt_mpc, UA)
        CA_anterior = np.concatenate(([CA_atual], CA_hist[:-1]))
        producao = (CA_anterior - CA_hist) * self.V  # mol de A convertidos por passo
        # UA*(Tj-T) é uma taxa (energia/min); multiplica por dt_mpc para obter a energia
        # efetivamente gasta naquele passo, na mesma base da produção por passo.
        carga_termica = np.abs(UA * (np.asarray(acoes_Tj) - T_hist)) * dt_mpc
        custo = self.custo_energia * carga_termica - self.preco_produto * producao
        return float(np.sum(custo))

    def _otimizar(self, funcao_custo, chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA):
        # Restrição de segurança: a trajetória prevista não pode ultrapassar o teto térmico.
        restricao_temp = NonlinearConstraint(
            lambda x, CA=CA_real, T=T_real: self.T_max_seguro - self._rollout_mpc(x, CA, T, dt_mpc, UA)[1],
            0, np.inf)
        # Restrição de atuador: a jaqueta não muda de temperatura instantaneamente.
        restricao_taxa = NonlinearConstraint(
            lambda x, Tj_ant=Tj_anterior: np.diff(np.concatenate(([Tj_ant], x))),
            -self.taxa_max_Tj, self.taxa_max_Tj)

        res = minimize(funcao_custo, chute_Tj, args=(CA_real, T_real, dt_mpc, UA),
                        bounds=[(self.Tj_min, self.Tj_max)] * len(chute_Tj),
                        constraints=[restricao_temp, restricao_taxa], method='SLSQP')
        return res.x

    def calcular_acao_controle(self, CA_atual, T_atual, Tj_anterior, economico=False,
                                dt_mpc=0.25, Hp=5, UA=None):
        """Resolve um único passo do MPC (rastreamento ou econômico) a partir do estado
        medido — a interface usada pela camada de integração (OPC-UA) para operar o reator
        em tempo real, um passo de cada vez, em vez de rodar uma simulação de ponta a ponta."""
        UA = self.UA_nominal if UA is None else UA
        funcao_custo = self._custo_economico if economico else self._custo_mpc
        chute_Tj = [Tj_anterior] * Hp
        Tj_otimizado = self._otimizar(funcao_custo, chute_Tj, CA_atual, T_atual, Tj_anterior, dt_mpc, UA)
        return float(Tj_otimizado[0])

    def rodar_mpc(self, UA=None, tempo_total=20, dt_mpc=0.25, Hp=5):
        UA = self.UA_nominal if UA is None else UA
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T, hist_Tj, hist_CA = np.zeros(passos), np.zeros(passos), np.zeros(passos)

        CA_real, T_real = self.CA_inicial, self.T_inicial
        chute_Tj = [self.T0 - 10.0] * Hp
        Tj_anterior = chute_Tj[0]

        for i in range(passos):
            hist_T[i], hist_Tj[i], hist_CA[i] = T_real, chute_Tj[0], CA_real

            Tj_otimizado = self._otimizar(self._custo_mpc, chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA)
            Tj_otimo = Tj_otimizado[0]
            chute_Tj = list(Tj_otimizado[1:]) + [Tj_otimizado[-1]]

            CA_real, T_real = self._rk4_step(CA_real, T_real, Tj_otimo, UA, dt_mpc)
            Tj_anterior = Tj_otimo

        return hist_tempo, hist_T, hist_Tj, hist_CA

    def rodar_mpc_economico(self, UA=None, tempo_total=20, dt_mpc=0.25, Hp=5):
        """Economic MPC: em vez de perseguir um setpoint de temperatura fixo e arbitrário
        (`T_alvo`), otimiza diretamente o resultado econômico — receita pela conversão de A
        menos custo energético da jaqueta —, respeitando as mesmas restrições de segurança
        (teto de temperatura e taxa do atuador) do MPC de rastreamento. Ilustra por que um
        setpoint fixo é só uma aproximação do que realmente importa para a planta."""
        UA = self.UA_nominal if UA is None else UA
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T, hist_Tj, hist_CA = np.zeros(passos), np.zeros(passos), np.zeros(passos)
        hist_lucro = np.zeros(passos)

        CA_real, T_real = self.CA_inicial, self.T_inicial
        chute_Tj = [self.T0 - 10.0] * Hp
        Tj_anterior = chute_Tj[0]

        for i in range(passos):
            hist_T[i], hist_Tj[i], hist_CA[i] = T_real, chute_Tj[0], CA_real

            Tj_otimizado = self._otimizar(self._custo_economico, chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA)
            Tj_otimo = Tj_otimizado[0]
            chute_Tj = list(Tj_otimizado[1:]) + [Tj_otimizado[-1]]

            CA_anterior = CA_real
            CA_real, T_real = self._rk4_step(CA_real, T_real, Tj_otimo, UA, dt_mpc)
            producao = (CA_anterior - CA_real) * self.V
            carga_termica = abs(UA * (Tj_otimo - T_real)) * dt_mpc
            hist_lucro[i] = self.preco_produto * producao - self.custo_energia * carga_termica
            Tj_anterior = Tj_otimo

        return hist_tempo, hist_T, hist_Tj, hist_CA, np.cumsum(hist_lucro)

    def rodar_mpc_com_deteccao_falha(self, UA_inicial=None, taxa_fouling=-1200.0, UA_minima=15000.0,
                                      tempo_total=40, dt_mpc=0.25, Hp=5,
                                      alpha_ewma=0.3, limiar_residuo=0.4):
        """Simula incrustação progressiva (fouling) na jaqueta: o UA real cai com o tempo,
        mas o modelo do MPC continua assumindo UA_inicial (como em uma planta real, onde a
        degradação não é conhecida a priori). Um detector por resíduo (EWMA do erro entre a
        temperatura medida e a prevista pelo modelo nominal) sinaliza a falha antes que o
        reator se aproxime do teto de segurança."""
        UA_inicial = self.UA_nominal if UA_inicial is None else UA_inicial
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T = np.zeros(passos)
        hist_Tj = np.zeros(passos)
        hist_UA_real = np.zeros(passos)
        hist_residuo = np.zeros(passos)
        tempo_deteccao = None

        CA_real, T_real = self.CA_inicial, self.T_inicial
        chute_Tj = [self.T0 - 10.0] * Hp
        Tj_anterior = chute_Tj[0]
        residuo_ewma = 0.0
        T_previsto_modelo = T_real

        for i in range(passos):
            UA_real_atual = max(UA_minima, UA_inicial + taxa_fouling * hist_tempo[i])
            hist_UA_real[i] = UA_real_atual

            residuo = abs(T_real - T_previsto_modelo)
            residuo_ewma = alpha_ewma * residuo + (1 - alpha_ewma) * residuo_ewma
            hist_residuo[i] = residuo_ewma
            if tempo_deteccao is None and residuo_ewma > limiar_residuo:
                tempo_deteccao = hist_tempo[i]

            hist_T[i], hist_Tj[i] = T_real, chute_Tj[0]

            Tj_otimizado = self._otimizar(self._custo_mpc, chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA_inicial)
            Tj_otimo = Tj_otimizado[0]
            chute_Tj = list(Tj_otimizado[1:]) + [Tj_otimizado[-1]]

            # O "gêmeo digital" prevê o próximo passo assumindo o UA nominal (sem saber do fouling).
            _, T_previsto_modelo = self._rk4_step(CA_real, T_real, Tj_otimo, UA_inicial, dt_mpc)
            # A planta real evolui com o UA degradado.
            CA_real, T_real = self._rk4_step(CA_real, T_real, Tj_otimo, UA_real_atual, dt_mpc)
            Tj_anterior = Tj_otimo

        return hist_tempo, hist_T, hist_Tj, hist_UA_real, hist_residuo, tempo_deteccao

    def simular_interlock_seguranca(self, UA=None, tempo_total=20, dt_mpc=0.25, Hp=5,
                                     DeltaH_real=-250000.0, usar_sis=True):
        """Camada de proteção independente (SIS — Sistema Instrumentado de Segurança),
        seguindo o conceito de "layers of protection" da IEC 61511: o MPC otimiza sua ação
        assumindo a cinética nominal (self.DeltaH), mas a planta real segue uma cinética mais
        severa (DeltaH_real) — por exemplo, uma impureza ou reação secundária não prevista na
        modelagem, causa raiz clássica de incidentes reais como Synthron (2006) e T2
        Laboratories (2007). Como o MPC só "enxerga" o mundo através do seu próprio modelo,
        sua restrição de segurança pode ser insuficiente diante desse descasamento. O SIS é
        um trip hard-wired independente do modelo do MPC: baseado diretamente na temperatura
        medida, força resfriamento máximo sempre que ela ultrapassa `T_trip_sis`."""
        UA = self.UA_nominal if UA is None else UA
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T = np.zeros(passos)
        hist_Tj_mpc = np.zeros(passos)
        hist_sis_ativo = np.zeros(passos, dtype=bool)
        tempo_trip = None

        CA_real, T_real = self.CA_inicial, self.T_inicial
        chute_Tj = [self.T0 - 10.0] * Hp
        Tj_anterior = chute_Tj[0]

        for i in range(passos):
            hist_T[i] = T_real

            Tj_otimizado = self._otimizar(self._custo_mpc, chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA)
            Tj_otimo = Tj_otimizado[0]
            chute_Tj = list(Tj_otimizado[1:]) + [Tj_otimizado[-1]]

            hist_Tj_mpc[i] = Tj_otimo
            if usar_sis:
                CA_real, T_real, trip_ocorreu = self._avancar_com_sis(CA_real, T_real, Tj_otimo, UA, dt_mpc,
                                                                        DeltaH_real)
                hist_sis_ativo[i] = trip_ocorreu
                if trip_ocorreu and tempo_trip is None:
                    tempo_trip = hist_tempo[i]
            else:
                CA_real, T_real = self._rk4_step(CA_real, T_real, Tj_otimo, UA, dt_mpc, DeltaH=DeltaH_real)
            Tj_anterior = Tj_otimo

        return hist_tempo, hist_T, hist_Tj_mpc, hist_sis_ativo, tempo_trip
