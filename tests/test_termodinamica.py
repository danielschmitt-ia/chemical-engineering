import pytest

from calculos_processo.termodinamica import (
    clausius_clapeyron_pressao,
    constante_equilibrio,
    energia_livre_gibbs_reacao,
    fator_compressibilidade,
    pressao_gas_ideal,
    pressao_vapor_antoine,
    temperatura_ebulicao_antoine,
)

# Constantes de Antoine da água (mmHg, °C), válidas de 1 a 100 °C.
A_AGUA, B_AGUA, C_AGUA = 8.07131, 1730.63, 233.426


class TestAntoine:
    def test_pressao_vapor_agua_a_100C_e_760_mmHg(self):
        assert pressao_vapor_antoine(A_AGUA, B_AGUA, C_AGUA, 100.0) == pytest.approx(760.0, abs=1.0)

    def test_temperatura_ebulicao_e_inversa_da_pressao_de_vapor(self):
        P = pressao_vapor_antoine(A_AGUA, B_AGUA, C_AGUA, 80.0)
        assert temperatura_ebulicao_antoine(A_AGUA, B_AGUA, C_AGUA, P) == pytest.approx(80.0, abs=1e-6)

    def test_pressao_de_vapor_cresce_com_temperatura(self):
        P_baixa = pressao_vapor_antoine(A_AGUA, B_AGUA, C_AGUA, 50.0)
        P_alta = pressao_vapor_antoine(A_AGUA, B_AGUA, C_AGUA, 90.0)
        assert P_alta > P_baixa


class TestGasIdeal:
    def test_pressao_gas_ideal(self):
        # 1 mol, 22.414 L a 273.15 K -> ~101325 Pa (volume molar padrão)
        P = pressao_gas_ideal(n=1.0, T=273.15, V=22.414e-3)
        assert P == pytest.approx(101325.0, rel=1e-3)

    def test_fator_compressibilidade_gas_ideal_e_um(self):
        P, T, n = 101325.0, 273.15, 1.0
        V = n * 8.314 * T / P
        assert fator_compressibilidade(P, V, n, T) == pytest.approx(1.0)


class TestEquilibrioQuimico:
    def test_reacao_espontanea_dG_negativo(self):
        assert energia_livre_gibbs_reacao(delta_H=-92000.0, T=298.15, delta_S=-198.0) < 0

    def test_constante_equilibrio_cresce_quando_dG_fica_mais_negativo(self):
        K1 = constante_equilibrio(delta_G=-10000.0, T=298.15)
        K2 = constante_equilibrio(delta_G=-30000.0, T=298.15)
        assert K2 > K1 > 0

    def test_dG_zero_da_K_igual_a_um(self):
        assert constante_equilibrio(delta_G=0.0, T=298.15) == pytest.approx(1.0)


class TestClausiusClapeyron:
    def test_pressao_igual_na_mesma_temperatura(self):
        assert clausius_clapeyron_pressao(101325.0, 373.15, 373.15, 40660.0) == pytest.approx(101325.0)

    def test_pressao_de_vapor_da_agua_a_90C_proxima_do_valor_tabelado(self):
        # ~70.1 kPa nas tabelas de vapor saturado; a aproximacao de Clausius-Clapeyron
        # (DeltaHvap constante) fica proxima, mas nao exata.
        P90 = clausius_clapeyron_pressao(101325.0, 373.15, 363.15, 40660.0)
        assert P90 == pytest.approx(70100.0, rel=0.02)

    def test_pressao_cai_com_temperatura_menor(self):
        P100 = clausius_clapeyron_pressao(101325.0, 373.15, 373.15, 40660.0)
        P80 = clausius_clapeyron_pressao(101325.0, 373.15, 353.15, 40660.0)
        assert P80 < P100
