import pytest

from calculos_processo.cristalizacao import (
    crescimento_cristal_lei_delta_L,
    rendimento_cristalizacao,
    supersaturacao_relativa,
)


class TestSupersaturacao:
    def test_solucao_saturada_e_zero(self):
        assert supersaturacao_relativa(100.0, 100.0) == pytest.approx(0.0)

    def test_supersaturada_e_positiva(self):
        assert supersaturacao_relativa(120.0, 100.0) == pytest.approx(0.2)


class TestCrescimentoDeltaL:
    def test_proporcional_ao_tempo(self):
        d1 = crescimento_cristal_lei_delta_L(2.0, 10.0)
        d2 = crescimento_cristal_lei_delta_L(2.0, 20.0)
        assert d2 == pytest.approx(2 * d1)


class TestRendimentoCristalizacao:
    def test_sem_evaporacao(self):
        Y = rendimento_cristalizacao(massa_alimentacao=1000.0, fracao_soluto_alimentacao=0.30,
                                      solubilidade_final=0.2, fracao_solvente_evaporada=0.0)
        soluto = 300.0
        solvente = 700.0
        cristais = soluto - 0.2 * solvente
        assert Y == pytest.approx(cristais / soluto)

    def test_evaporacao_aumenta_rendimento(self):
        Y_sem_evap = rendimento_cristalizacao(1000.0, 0.30, 0.2, fracao_solvente_evaporada=0.0)
        Y_com_evap = rendimento_cristalizacao(1000.0, 0.30, 0.2, fracao_solvente_evaporada=0.3)
        assert Y_com_evap > Y_sem_evap

    def test_solubilidade_menor_aumenta_rendimento(self):
        Y_soluvel = rendimento_cristalizacao(1000.0, 0.30, 0.5, 0.0)
        Y_pouco_soluvel = rendimento_cristalizacao(1000.0, 0.30, 0.05, 0.0)
        assert Y_pouco_soluvel > Y_soluvel
