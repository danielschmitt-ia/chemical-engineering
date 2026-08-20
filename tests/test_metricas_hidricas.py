import pytest

from calculos_processo.metricas_hidricas import intensidade_hidrica, taxa_reuso_agua


class TestIntensidadeHidrica:
    def test_formula_direta(self):
        assert intensidade_hidrica(volume_agua_consumida=500.0, producao=1000.0) == pytest.approx(0.5)


class TestTaxaReuso:
    def test_formula_direta(self):
        assert taxa_reuso_agua(volume_agua_reusada=300.0, volume_agua_total_utilizada=500.0) == pytest.approx(0.6)

    def test_sem_reuso_e_zero(self):
        assert taxa_reuso_agua(0.0, 500.0) == pytest.approx(0.0)

    def test_reuso_total_e_um(self):
        assert taxa_reuso_agua(500.0, 500.0) == pytest.approx(1.0)
