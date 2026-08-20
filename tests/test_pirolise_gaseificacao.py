import pytest

from calculos_processo.pirolise_gaseificacao import eficiencia_gas_frio


class TestEficienciaGasFrio:
    def test_formula_direta(self):
        CGE = eficiencia_gas_frio(massa_gas=800.0, pci_gas=12.0, massa_biomassa=1000.0, pci_biomassa=18.0)
        assert CGE == pytest.approx((800.0 * 12.0) / (1000.0 * 18.0))

    def test_menos_gas_produzido_reduz_cge(self):
        CGE_bom = eficiencia_gas_frio(800.0, 12.0, 1000.0, 18.0)
        CGE_ruim = eficiencia_gas_frio(500.0, 12.0, 1000.0, 18.0)
        assert CGE_ruim < CGE_bom
