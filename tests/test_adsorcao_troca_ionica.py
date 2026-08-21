import pytest

from calculos_processo.adsorcao_troca_ionica import (
    isoterma_freundlich,
    isoterma_langmuir,
    tempo_ruptura_estequiometrico,
)


class TestLangmuir:
    def test_baixa_concentracao_aproxima_linear(self):
        q = isoterma_langmuir(C=0.001, q_max=10.0, K=5.0)
        assert q == pytest.approx(10.0 * 5.0 * 0.001, rel=1e-2)

    def test_alta_concentracao_satura_em_qmax(self):
        q = isoterma_langmuir(C=1e6, q_max=10.0, K=5.0)
        assert q == pytest.approx(10.0, rel=1e-3)

    def test_monotonica_crescente(self):
        q1 = isoterma_langmuir(1.0, 10.0, 2.0)
        q2 = isoterma_langmuir(5.0, 10.0, 2.0)
        assert q2 > q1


class TestFreundlich:
    def test_n_igual_um_e_linear(self):
        assert isoterma_freundlich(C=3.0, Kf=2.0, n=1.0) == pytest.approx(6.0)

    def test_monotonica_crescente(self):
        q1 = isoterma_freundlich(1.0, 2.0, 2.0)
        q2 = isoterma_freundlich(4.0, 2.0, 2.0)
        assert q2 > q1


class TestTempoRuptura:
    def test_formula_direta(self):
        t = tempo_ruptura_estequiometrico(massa_adsorvente=100.0, capacidade_adsorcao=0.05,
                                           vazao_massica_soluto=0.001)
        assert t == pytest.approx(5000.0)

    def test_mais_adsorvente_aumenta_tempo(self):
        t_pouco = tempo_ruptura_estequiometrico(50.0, 0.05, 0.001)
        t_muito = tempo_ruptura_estequiometrico(200.0, 0.05, 0.001)
        assert t_muito > t_pouco
