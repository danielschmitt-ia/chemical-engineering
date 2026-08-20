import pytest

from calculos_processo.engenharia_corrosao import taxa_corrosao


class TestTaxaCorrosao:
    def test_formula_direta(self):
        taxa = taxa_corrosao(perda_massa=0.5, densidade=7.87, area_exposta=10.0, tempo_exposicao=1.0)
        assert taxa == pytest.approx(0.5 / (7.87 * 10.0 * 1.0))

    def test_mais_perda_de_massa_aumenta_taxa(self):
        taxa_baixa = taxa_corrosao(0.1, 7.87, 10.0, 1.0)
        taxa_alta = taxa_corrosao(0.5, 7.87, 10.0, 1.0)
        assert taxa_alta > taxa_baixa

    def test_maior_tempo_de_exposicao_reduz_taxa_calculada(self):
        # mesma perda de massa total, mas espalhada por mais tempo -> taxa media menor
        taxa_curto = taxa_corrosao(0.5, 7.87, 10.0, 1.0)
        taxa_longo = taxa_corrosao(0.5, 7.87, 10.0, 5.0)
        assert taxa_longo < taxa_curto
