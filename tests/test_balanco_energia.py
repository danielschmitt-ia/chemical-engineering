import pytest

from calculos_processo.balanco_energia import (
    balanco_energia_escoamento,
    energia_cinetica_especifica,
    energia_potencial_especifica,
    residuo_balanco_energia_global,
)


class TestEnergiasEspecificas:
    def test_energia_cinetica(self):
        assert energia_cinetica_especifica(4.0) == pytest.approx(8.0)

    def test_energia_potencial(self):
        assert energia_potencial_especifica(10.0, g=9.81) == pytest.approx(98.1)


class TestBalancoEnergiaEscoamento:
    def test_somente_entalpia_quando_ec_ep_desprezaveis(self):
        assert balanco_energia_escoamento(delta_h=5000.0) == pytest.approx(5000.0)

    def test_inclui_variacao_de_cota(self):
        q_menos_w = balanco_energia_escoamento(delta_h=0.0, z_entrada=0.0, z_saida=10.0, g=9.81)
        assert q_menos_w == pytest.approx(98.1)

    def test_inclui_variacao_de_velocidade(self):
        q_menos_w = balanco_energia_escoamento(delta_h=0.0, v_entrada=0.0, v_saida=10.0)
        assert q_menos_w == pytest.approx(50.0)


class TestResiduoBalancoEnergiaGlobal:
    def test_zero_quando_fecha(self):
        assert residuo_balanco_energia_global([1000.0, 500.0], [1500.0]) == pytest.approx(0.0)

    def test_positivo_quando_falta_saida(self):
        assert residuo_balanco_energia_global([1000.0], [400.0]) == pytest.approx(600.0)
