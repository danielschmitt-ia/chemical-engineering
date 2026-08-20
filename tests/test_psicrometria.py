import pytest

from calculos_processo.psicrometria import (
    approach_torre_resfriamento,
    range_torre_resfriamento,
    razao_umidade,
    umidade_relativa,
)


class TestRazaoUmidade:
    def test_formula_direta(self):
        W = razao_umidade(pressao_vapor_agua=1500.0, pressao_total=101325.0)
        assert W == pytest.approx(0.622 * 1500.0 / (101325.0 - 1500.0))

    def test_mais_vapor_aumenta_razao_umidade(self):
        W_seco = razao_umidade(500.0, 101325.0)
        W_umido = razao_umidade(3000.0, 101325.0)
        assert W_umido > W_seco


class TestUmidadeRelativa:
    def test_saturacao_e_cem_por_cento(self):
        assert umidade_relativa(pressao_vapor_agua=2339.0, pressao_vapor_saturacao=2339.0) == pytest.approx(1.0)

    def test_metade_da_saturacao(self):
        assert umidade_relativa(1169.5, 2339.0) == pytest.approx(0.5)


class TestTorreResfriamento:
    def test_range(self):
        assert range_torre_resfriamento(T_agua_quente_entrada=40.0, T_agua_fria_saida=30.0) == pytest.approx(10.0)

    def test_approach(self):
        assert approach_torre_resfriamento(T_agua_fria_saida=30.0, T_bulbo_umido_ar=25.0) == pytest.approx(5.0)

    def test_approach_menor_exige_torre_melhor_mas_e_so_a_diferenca(self):
        # approach pequeno = agua sai bem perto do bulbo umido (torre eficiente/bem dimensionada)
        approach_grande = approach_torre_resfriamento(35.0, 25.0)
        approach_pequeno = approach_torre_resfriamento(26.0, 25.0)
        assert approach_pequeno < approach_grande
