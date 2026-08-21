import pytest

from calculos_processo.integracao_processos_pinch import tabela_problema_pinch


class TestTabelaProblemaPinch:
    def test_caso_com_pinch_verificado_manualmente(self):
        # H1: 200->100 CP=2 (libera 200 kW); C1: 50->150 CP=3 (precisa de 300 kW).
        # dTmin=20. Conferido manualmente (cascata sem utilidade: [0,60,-10,-100]).
        r = tabela_problema_pinch([(200, 100, 2.0)], [(50, 150, 3.0)], delta_t_min=20.0)
        assert r["utilidade_quente_minima"] == pytest.approx(100.0)
        assert r["utilidade_fria_minima"] == pytest.approx(0.0)
        assert r["temperatura_pinch_quente"] == pytest.approx(70.0)
        assert r["temperatura_pinch_fria"] == pytest.approx(50.0)
        assert r["temperatura_pinch_quente"] - r["temperatura_pinch_fria"] == pytest.approx(20.0)

    def test_balanco_de_energia_global_fecha(self):
        # utilidade_quente + duty_das_quentes == duty_das_frias + utilidade_fria (conservacao de energia)
        quentes = [(200.0, 100.0, 2.0), (170.0, 60.0, 1.0)]
        frias = [(50.0, 150.0, 3.0), (30.0, 90.0, 1.5)]
        r = tabela_problema_pinch(quentes, frias, delta_t_min=10.0)
        duty_quente = sum(CP * (Ts - Tt) for Ts, Tt, CP in quentes)
        duty_fria = sum(CP * (Tt - Ts) for Ts, Tt, CP in frias)
        assert r["utilidade_quente_minima"] + duty_quente == pytest.approx(duty_fria + r["utilidade_fria_minima"])

    def test_cascata_viavel_nunca_negativa(self):
        quentes = [(200.0, 100.0, 2.0), (170.0, 60.0, 1.0)]
        frias = [(50.0, 150.0, 3.0), (30.0, 90.0, 1.5)]
        r = tabela_problema_pinch(quentes, frias, delta_t_min=10.0)
        assert all(c >= -1e-9 for c in r["cascata_viavel"])

    def test_deltatmin_maior_nunca_reduz_a_utilidade_minima(self):
        # aumentar a aproximacao minima exigida so pode piorar (ou manter) a meta de utilidade
        quentes = [(200.0, 100.0, 2.0)]
        frias = [(50.0, 150.0, 3.0)]
        r_apertado = tabela_problema_pinch(quentes, frias, delta_t_min=5.0)
        r_folgado = tabela_problema_pinch(quentes, frias, delta_t_min=40.0)
        assert r_folgado["utilidade_quente_minima"] >= r_apertado["utilidade_quente_minima"]

    def test_streams_balanceadas_no_limiar_nao_exigem_utilidade(self):
        # H1 e C1 com mesma duty total e CPs iguais, dTmin exatamente conciliavel: caso limite
        # (threshold problem) onde tanto utilidade quente quanto fria minimas sao zero.
        r = tabela_problema_pinch([(200.0, 100.0, 2.0)], [(60.0, 160.0, 2.0)], delta_t_min=20.0)
        assert r["utilidade_quente_minima"] == pytest.approx(0.0)
        assert r["utilidade_fria_minima"] == pytest.approx(0.0)
