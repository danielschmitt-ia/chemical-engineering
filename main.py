import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import minimize, NonlinearConstraint
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class ReatorCSTR:
    def __init__(self):
        self.V = 100.0        # Volume do reator (L)
        self.F = 10.0         # Vazão volumétrica (L/min)
        self.CA0 = 2.0        # Concentração de entrada de A (mol/L)
        self.T0 = 300.0       # Temperatura de entrada (K)
        self.Pre_exp_A = 7.2e10 # Fator Arrhenius (1/min)
        self.Ea_R = 8750.0    # Ea/R (K)
        self.DeltaH = -50000.0 # Calor de reação (J/mol)
        self.rho = 1000.0     # Densidade (g/L)
        self.Cp = 4.184       # Cp (J/g·K)
        self.T_alvo = 330.0   # Setpoint do MPC (K)
        self.T_max_seguro = 345.0  # Teto de segurança imposto ao MPC (K)
        self.taxa_max_Tj = 5.0     # Limite de variação de Tj por passo de controle (K)

    def calcular_cinetica(self, CA, T):
        k = self.Pre_exp_A * np.exp(-self.Ea_R / T)
        return k * CA

    def _derivadas(self, CA, T, Tj, UA):
        CA = max(CA, 0.0)
        taxa = self.calcular_cinetica(CA, T)
        dCAdt = (self.F / self.V) * (self.CA0 - CA) - taxa
        dTdt = ((self.F / self.V) * (self.T0 - T)) + ((-self.DeltaH * taxa) / (self.rho * self.Cp)) + ((UA * (Tj - T)) / (self.V * self.rho * self.Cp))
        return dCAdt, dTdt

    def _dinamica_ivp(self, t, y, Tj, UA):
        return self._derivadas(y[0], y[1], Tj, UA)

    def _rk4_step(self, CA, T, Tj, UA, dt):
        k1_CA, k1_T = self._derivadas(CA, T, Tj, UA)
        k2_CA, k2_T = self._derivadas(CA + dt / 2 * k1_CA, T + dt / 2 * k1_T, Tj, UA)
        k3_CA, k3_T = self._derivadas(CA + dt / 2 * k2_CA, T + dt / 2 * k2_T, Tj, UA)
        k4_CA, k4_T = self._derivadas(CA + dt * k3_CA, T + dt * k3_T, Tj, UA)
        CA_novo = CA + (dt / 6) * (k1_CA + 2 * k2_CA + 2 * k3_CA + k4_CA)
        T_novo = T + (dt / 6) * (k1_T + 2 * k2_T + 2 * k3_T + k4_T)
        return max(0.0, CA_novo), T_novo

    def simular_runaway(self, UA_operacao, Tj=290.0, tempo_total=20, dt=0.02):
        # Integração adaptativa (RK45) em vez de Euler explícito: essencial perto do
        # runaway, onde a dinâmica fica rígida (stiff) e o passo fixo perde precisão.
        hist_tempo = np.arange(0, tempo_total, dt)

        def evento_runaway(t, y, Tj, UA):
            return 600.0 - y[1]
        evento_runaway.terminal = True
        evento_runaway.direction = -1

        sol = solve_ivp(self._dinamica_ivp, [0, tempo_total], [2.0, 300.0], t_eval=hist_tempo,
                         args=(Tj, UA_operacao), method='RK45', max_step=dt, events=evento_runaway)

        hist_T = np.full(len(hist_tempo), sol.y[1, -1])
        hist_T[:sol.t.size] = sol.y[1]
        return hist_tempo, hist_T

    def _rollout_mpc(self, acoes_Tj, CA_atual, T_atual, dt_mpc, UA):
        CA_pred, T_pred = CA_atual, T_atual
        T_hist = np.zeros(len(acoes_Tj))
        for idx, Tj_predito in enumerate(acoes_Tj):
            CA_pred, T_pred = self._rk4_step(CA_pred, T_pred, Tj_predito, UA, dt_mpc)
            T_hist[idx] = T_pred
        return CA_pred, T_hist

    def _custo_mpc(self, acoes_Tj, CA_atual, T_atual, dt_mpc, UA):
        _, T_pred = self._rollout_mpc(acoes_Tj, CA_atual, T_atual, dt_mpc, UA)
        return float(np.sum((T_pred - self.T_alvo) ** 2))

    def _otimizar_mpc(self, chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA):
        # Restrição de segurança: a trajetória prevista não pode ultrapassar o teto térmico.
        restricao_temp = NonlinearConstraint(
            lambda x, CA=CA_real, T=T_real: self.T_max_seguro - self._rollout_mpc(x, CA, T, dt_mpc, UA)[1],
            0, np.inf)
        # Restrição de atuador: a jaqueta não muda de temperatura instantaneamente.
        restricao_taxa = NonlinearConstraint(
            lambda x, Tj_ant=Tj_anterior: np.diff(np.concatenate(([Tj_ant], x))),
            -self.taxa_max_Tj, self.taxa_max_Tj)

        res = minimize(self._custo_mpc, chute_Tj, args=(CA_real, T_real, dt_mpc, UA),
                        bounds=[(240.0, 350.0)] * len(chute_Tj),
                        constraints=[restricao_temp, restricao_taxa], method='SLSQP')
        return res.x

    def rodar_mpc(self, UA=50000.0, tempo_total=20, dt_mpc=0.25, Hp=5):
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T, hist_Tj, hist_CA = np.zeros(passos), np.zeros(passos), np.zeros(passos)

        CA_real, T_real = 2.0, 300.0
        chute_Tj = [290.0] * Hp
        Tj_anterior = 290.0

        for i in range(passos):
            hist_T[i], hist_Tj[i], hist_CA[i] = T_real, chute_Tj[0], CA_real

            Tj_otimizado = self._otimizar_mpc(chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA)
            Tj_otimo = Tj_otimizado[0]
            chute_Tj = list(Tj_otimizado[1:]) + [Tj_otimizado[-1]]

            CA_real, T_real = self._rk4_step(CA_real, T_real, Tj_otimo, UA, dt_mpc)
            Tj_anterior = Tj_otimo

        return hist_tempo, hist_T, hist_Tj, hist_CA

    def rodar_mpc_com_deteccao_falha(self, UA_inicial=50000.0, taxa_fouling=-1200.0, UA_minima=15000.0,
                                      tempo_total=40, dt_mpc=0.25, Hp=5,
                                      alpha_ewma=0.3, limiar_residuo=0.4):
        """Simula incrustação progressiva (fouling) na jaqueta: o UA real cai com o tempo,
        mas o modelo do MPC continua assumindo UA_inicial (como em uma planta real, onde a
        degradação não é conhecida a priori). Um detector por resíduo (EWMA do erro entre a
        temperatura medida e a prevista pelo modelo nominal) sinaliza a falha antes que o
        reator se aproxime do teto de segurança."""
        passos = int(tempo_total / dt_mpc)
        hist_tempo = np.linspace(0, tempo_total, passos)
        hist_T = np.zeros(passos)
        hist_Tj = np.zeros(passos)
        hist_UA_real = np.zeros(passos)
        hist_residuo = np.zeros(passos)
        tempo_deteccao = None

        CA_real, T_real = 2.0, 300.0
        chute_Tj = [290.0] * Hp
        Tj_anterior = 290.0
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

            Tj_otimizado = self._otimizar_mpc(chute_Tj, CA_real, T_real, Tj_anterior, dt_mpc, UA_inicial)
            Tj_otimo = Tj_otimizado[0]
            chute_Tj = list(Tj_otimizado[1:]) + [Tj_otimizado[-1]]

            # O "gêmeo digital" prevê o próximo passo assumindo o UA nominal (sem saber do fouling).
            _, T_previsto_modelo = self._rk4_step(CA_real, T_real, Tj_otimo, UA_inicial, dt_mpc)
            # A planta real evolui com o UA degradado.
            CA_real, T_real = self._rk4_step(CA_real, T_real, Tj_otimo, UA_real_atual, dt_mpc)
            Tj_anterior = Tj_otimo

        return hist_tempo, hist_T, hist_Tj, hist_UA_real, hist_residuo, tempo_deteccao

if __name__ == "__main__":
    print("🚀 Executando simulação integrada...")
    reator = ReatorCSTR()
    t1, T_seguro = reator.simular_runaway(UA_operacao=50000.0)
    _, T_critico = reator.simular_runaway(UA_operacao=32000.0)
    t2, hist_T_mpc, hist_Tj_mpc, hist_CA_mpc = reator.rodar_mpc()

    X_dados = (hist_T_mpc + np.random.normal(0, 0.4, size=len(hist_T_mpc))).reshape(-1, 1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_dados)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, hist_CA_mpc, test_size=0.2, random_state=42)

    ia_sensor = MLPRegressor(hidden_layer_sizes=(15, 10), max_iter=2000, random_state=42)
    ia_sensor.fit(X_train, y_train)
    concentracao_predita = ia_sensor.predict(X_scaled)

    print("🔎 Executando cenário de fouling com detecção de falha...")
    t3, T_falha, Tj_falha, UA_real_falha, residuo_falha, tempo_deteccao = reator.rodar_mpc_com_deteccao_falha()
    if tempo_deteccao is not None:
        print(f"⚠️  Degradação de UA detectada em t = {tempo_deteccao:.2f} min "
              f"(UA real na detecção ≈ {UA_real_falha[np.searchsorted(t3, tempo_deteccao)]:.0f})")
    else:
        print("✅ Nenhuma falha detectada no horizonte simulado.")

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    ax1.plot(t1, T_seguro, label='Seguro')
    ax1.plot(t1, T_critico, '--', label='Runaway')
    ax1.set_title('Fuga Térmica (Runaway) — integração RK45')
    ax1.set_xlabel('Tempo (min)'); ax1.set_ylabel('Temperatura (K)')
    ax1.legend(); ax1.grid(True)
    fig1.tight_layout(); fig1.savefig('estabilidade_runaway.png', dpi=150)

    fig2, axs2 = plt.subplots(2, 1, figsize=(10, 8))
    axs2[0].plot(t2, hist_T_mpc, color='purple', label='T (MPC)')
    axs2[0].axhline(y=reator.T_alvo, color='black', linestyle=':', label='Setpoint')
    axs2[0].axhline(y=reator.T_max_seguro, color='red', linestyle='--', label='Teto de segurança')
    axs2[0].set_title('MPC com restrições de segurança (temperatura e taxa do atuador)')
    axs2[0].legend(); axs2[0].grid(True)

    axs2[1].plot(t2, hist_CA_mpc, label='Real')
    axs2[1].plot(t2, concentracao_predita, '--', label='IA (soft sensor)')
    axs2[1].set_title('Soft Sensor (Rede Neural)')
    axs2[1].legend(); axs2[1].grid(True)
    fig2.tight_layout(); fig2.savefig('mpc_softsensor.png', dpi=150)

    fig3, axs3 = plt.subplots(2, 1, figsize=(10, 8))
    axs3[0].plot(t3, UA_real_falha, color='darkorange', label='UA real (fouling)')
    axs3[0].axhline(y=50000.0, color='gray', linestyle=':', label='UA nominal do modelo')
    if tempo_deteccao is not None:
        axs3[0].axvline(x=tempo_deteccao, color='red', linestyle='--', label='Falha detectada')
    axs3[0].set_title('Degradação simulada do coeficiente de troca térmica (UA)')
    axs3[0].legend(); axs3[0].grid(True)

    axs3[1].plot(t3, residuo_falha, color='crimson', label='Resíduo (EWMA)')
    axs3[1].axhline(y=0.4, color='black', linestyle=':', label='Limiar de alarme')
    if tempo_deteccao is not None:
        axs3[1].axvline(x=tempo_deteccao, color='red', linestyle='--')
    axs3[1].set_title('Detecção de Falha por Resíduo do Gêmeo Digital')
    axs3[1].legend(); axs3[1].grid(True)
    fig3.tight_layout(); fig3.savefig('deteccao_falha.png', dpi=150)

    plt.show()
