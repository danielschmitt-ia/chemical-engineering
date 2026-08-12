import numpy as np
import pytest

from reator_digital_twin import ReatorCSTR


def test_calcular_cinetica_cresce_com_temperatura(reator):
    k_frio = reator.calcular_cinetica(CA=1.0, T=300.0)
    k_quente = reator.calcular_cinetica(CA=1.0, T=340.0)
    assert k_quente > k_frio > 0


def test_calcular_cinetica_proporcional_a_CA(reator):
    assert reator.calcular_cinetica(CA=2.0, T=320.0) == pytest.approx(
        2 * reator.calcular_cinetica(CA=1.0, T=320.0))


class TestRunaway:
    def test_cenario_seguro_permanece_estavel(self, reator):
        _, T = reator.simular_runaway(UA_operacao=50000.0, tempo_total=20)
        assert T.max() < 320.0  # bem abaixo do teto de segurança (345 K)

    def test_cenario_critico_diverge(self, reator):
        _, T_seguro = reator.simular_runaway(UA_operacao=50000.0, tempo_total=20)
        _, T_critico = reator.simular_runaway(UA_operacao=32000.0, tempo_total=20)
        # cinética de pior caso (DeltaH_cenario) com UA degradado: fuga térmica real,
        # bem acima do que a cinética nominal usada pelo controle jamais atingiria.
        assert T_critico.max() > 380.0
        assert T_critico.max() > T_seguro.max()

    def test_nao_ultrapassa_evento_de_seguranca(self, reator):
        # O evento de parada em 600 K existe para cenários extremos; com os parâmetros
        # ilustrativos deste projeto não deve disparar.
        _, T_critico = reator.simular_runaway(UA_operacao=32000.0, tempo_total=20)
        assert T_critico.max() < 600.0


class TestMPCRastreamento:
    def test_converge_para_o_setpoint(self, reator):
        _, T, _, _ = reator.rodar_mpc(tempo_total=20)
        assert T[-5:] == pytest.approx(reator.T_alvo, abs=1.0)

    def test_respeita_teto_de_seguranca(self, reator):
        _, T, _, _ = reator.rodar_mpc(tempo_total=20)
        assert T.max() <= reator.T_max_seguro + 1e-6

    def test_respeita_taxa_maxima_do_atuador(self, reator):
        # hist_Tj de rodar_mpc registra o *chute* do horizonte antes de otimizar, não a
        # ação de fato aplicada ao atuador (só o primeiro elemento de cada horizonte
        # otimizado é aplicado) — não é o sinal certo para checar essa restrição. Refaz o
        # loop capturando diretamente a sequência de ações efetivamente aplicadas.
        CA, T = reator.CA_inicial, reator.T_inicial
        Tj_anterior = reator.T0 - 10.0
        chute = None
        aplicados = []
        for _ in range(80):
            Tj_otimo, chute = reator.calcular_acao_controle(CA, T, Tj_anterior, chute_horizonte=chute)
            aplicados.append(Tj_otimo)
            CA, T = reator._rk4_step(CA, T, Tj_otimo, reator.UA_nominal, 0.25)
            Tj_anterior = Tj_otimo

        variacoes = np.abs(np.diff(aplicados))
        assert variacoes.max() <= reator.taxa_max_Tj + 1e-6

    def test_concentracao_nao_negativa(self, reator):
        _, _, _, CA = reator.rodar_mpc(tempo_total=20)
        assert (CA >= 0).all()


class TestMPCEconomico:
    def test_lucro_acumulado_positivo(self, reator):
        _, _, _, _, lucro = reator.rodar_mpc_economico(tempo_total=20)
        assert lucro[-1] > 0

    def test_respeita_teto_de_seguranca(self, reator):
        _, T, _, _, _ = reator.rodar_mpc_economico(tempo_total=20)
        assert T.max() <= reator.T_max_seguro + 1e-6

    def test_encontra_ponto_diferente_do_setpoint_fixo(self, reator):
        # O ponto ótimo econômico (para os preços ilustrativos deste projeto) fica acima
        # do setpoint fixo do MPC de rastreamento — essa é a demonstração central do
        # Economic MPC (ver README).
        _, T, _, _, _ = reator.rodar_mpc_economico(tempo_total=20)
        assert T[-5:].mean() > reator.T_alvo


class TestDeteccaoDeFalha:
    def test_sinaliza_degradacao_de_UA(self, reator):
        _, T, _, UA_real, residuo, tempo_deteccao = reator.rodar_mpc_com_deteccao_falha()
        assert tempo_deteccao is not None
        assert UA_real[-1] < UA_real[0]  # UA de fato degradou ao longo do cenário

    def test_sem_fouling_nao_dispara_alarme(self, reator):
        _, T, _, UA_real, residuo, tempo_deteccao = reator.rodar_mpc_com_deteccao_falha(
            taxa_fouling=0.0, tempo_total=15)
        assert tempo_deteccao is None

    def test_temperatura_permanece_controlada_apesar_da_falha(self, reator):
        # A degradação é sinalizada bem antes de virar um evento de segurança — a
        # temperatura deve seguir dentro do envelope seguro durante todo o cenário.
        _, T, _, _, _, _ = reator.rodar_mpc_com_deteccao_falha()
        assert T.max() <= reator.T_max_seguro + 1.0


class TestInterlockSIS:
    def test_sem_sis_a_planta_diverge_sob_descasamento_de_modelo(self, reator):
        _, T, _, _, _ = reator.simular_interlock_seguranca(usar_sis=False, tempo_total=20)
        assert T.max() > 380.0

    def test_com_sis_a_planta_fica_contida(self, reator):
        _, T, _, _, tempo_trip = reator.simular_interlock_seguranca(usar_sis=True, tempo_total=20)
        assert tempo_trip is not None
        assert T.max() < 330.0  # bem contido, longe do pico sem SIS (>380 K)

    def test_sis_dispara_antes_do_ponto_sem_retorno(self, reator):
        _, T, _, _, tempo_trip = reator.simular_interlock_seguranca(usar_sis=True, tempo_total=20)
        assert tempo_trip < 10.0  # dispara cedo no cenário (~t=3.5 min nas demos)


class TestCalcularAcaoControle:
    def test_bate_com_rodar_mpc_em_lote(self, reator):
        """Regressão: calcular_acao_controle (usado pela integração OPC-UA) precisa
        reproduzir a mesma trajetória que rodar_mpc (usado pelas demos em lote) quando
        alimentado com o mesmo warm-start — divergiram no passado por essa razão."""
        _, T_lote, Tj_lote, _ = reator.rodar_mpc(tempo_total=8)

        CA, T = reator.CA_inicial, reator.T_inicial
        Tj_anterior = reator.T0 - 10.0
        chute = None
        T_manual = []
        for _ in range(len(T_lote)):
            # registra ANTES de aplicar a ação, como rodar_mpc faz (hist_T[i] é o estado no
            # início do ciclo i, não depois de aplicar a ação decidida nesse ciclo).
            T_manual.append(T)
            Tj_otimo, chute = reator.calcular_acao_controle(CA, T, Tj_anterior, chute_horizonte=chute)
            CA, T = reator._rk4_step(CA, T, Tj_otimo, reator.UA_nominal, 0.25)
            Tj_anterior = Tj_otimo

        assert np.allclose(T_manual, T_lote, atol=0.5)

    def test_warm_start_e_reaproveitado(self, reator):
        Tj_otimo1, chute1 = reator.calcular_acao_controle(2.0, 300.0, 290.0)
        Tj_otimo2, chute2 = reator.calcular_acao_controle(1.98, 300.5, Tj_otimo1, chute_horizonte=chute1)
        assert len(chute1) == len(chute2) == 5
