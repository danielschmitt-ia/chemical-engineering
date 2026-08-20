import pytest

from calculos_processo.analise_financeira_projetos import (
    payback_simples,
    taxa_interna_retorno,
    valor_presente_liquido,
)


class TestVPL:
    def test_taxa_zero_e_soma_simples_dos_fluxos(self):
        fluxos = [-1000.0, 300.0, 400.0, 500.0]
        assert valor_presente_liquido(fluxos, taxa_desconto=0.0) == pytest.approx(sum(fluxos))

    def test_taxa_maior_reduz_vpl_de_fluxos_futuros_positivos(self):
        fluxos = [-1000.0, 300.0, 400.0, 500.0, 300.0]
        VPL_taxa_baixa = valor_presente_liquido(fluxos, 0.05)
        VPL_taxa_alta = valor_presente_liquido(fluxos, 0.20)
        assert VPL_taxa_alta < VPL_taxa_baixa

    def test_apenas_investimento_negativo(self):
        assert valor_presente_liquido([-1000.0], 0.10) == pytest.approx(-1000.0)


class TestPayback:
    def test_formula_direta(self):
        assert payback_simples(investimento_inicial=1000.0, fluxo_caixa_anual=250.0) == pytest.approx(4.0)


class TestTIR:
    def test_vpl_na_tir_e_zero(self):
        fluxos = [-1000.0, 300.0, 400.0, 500.0, 300.0]
        TIR = taxa_interna_retorno(fluxos)
        assert valor_presente_liquido(fluxos, TIR) == pytest.approx(0.0, abs=1e-8)

    def test_projeto_com_retorno_maior_tem_tir_maior(self):
        fluxos_modesto = [-1000.0, 300.0, 300.0, 300.0, 300.0]
        fluxos_otimo = [-1000.0, 500.0, 500.0, 500.0, 500.0]
        TIR_modesto = taxa_interna_retorno(fluxos_modesto)
        TIR_otimo = taxa_interna_retorno(fluxos_otimo)
        assert TIR_otimo > TIR_modesto
