import pytest

from calculos_processo.geracao_vapor import (
    eficiencia_caldeira,
    eficiencia_global_cogeracao,
    heat_rate_cogeracao,
)


class TestEficienciaCaldeira:
    def test_formula_direta(self):
        eta = eficiencia_caldeira(vazao_vapor=10000.0, entalpia_vapor=2800.0,
                                   entalpia_agua_alimentacao=420.0, vazao_combustivel=1000.0,
                                   pci_combustivel=42000.0)
        assert eta == pytest.approx((10000.0 * (2800.0 - 420.0)) / (1000.0 * 42000.0))

    def test_mais_combustivel_para_mesmo_vapor_reduz_eficiencia(self):
        eta_bom = eficiencia_caldeira(10000.0, 2800.0, 420.0, 1000.0, 42000.0)
        eta_ruim = eficiencia_caldeira(10000.0, 2800.0, 420.0, 1300.0, 42000.0)
        assert eta_ruim < eta_bom


class TestCogeracao:
    def test_heat_rate(self):
        assert heat_rate_cogeracao(energia_combustivel=3.0, potencia_eletrica=1.0) == pytest.approx(3.0)

    def test_eficiencia_global_maior_que_so_eletrica(self):
        eficiencia_eletrica = 1.0 / 3.0
        eficiencia_global = eficiencia_global_cogeracao(potencia_eletrica=1.0, calor_util=1.5, energia_combustivel=3.0)
        assert eficiencia_global > eficiencia_eletrica
