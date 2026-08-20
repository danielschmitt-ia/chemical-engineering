import pytest

from calculos_processo.balanco_carbono import emissao_co2_combustao, intensidade_carbono


class TestEmissaoCO2:
    def test_formula_direta(self):
        co2 = emissao_co2_combustao(massa_combustivel=1000.0, fracao_massica_carbono=0.87)
        assert co2 == pytest.approx(1000.0 * 0.87 * (44.01 / 12.011))

    def test_sem_carbono_emissao_zero(self):
        assert emissao_co2_combustao(1000.0, 0.0) == pytest.approx(0.0)

    def test_massa_co2_maior_que_massa_carbono(self):
        # cada atomo de carbono "ganha" massa ao virar CO2 (adiciona 2 oxigenios)
        massa_carbono = 1000.0 * 0.87
        co2 = emissao_co2_combustao(1000.0, 0.87)
        assert co2 > massa_carbono


class TestIntensidadeCarbono:
    def test_formula_direta(self):
        assert intensidade_carbono(emissao_co2=500.0, producao=100.0) == pytest.approx(5.0)
