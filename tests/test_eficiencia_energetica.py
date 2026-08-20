import pytest

from calculos_processo.eficiencia_energetica import consumo_especifico_energia


class TestSEC:
    def test_formula_direta(self):
        assert consumo_especifico_energia(energia_consumida=5000.0, producao=1000.0) == pytest.approx(5.0)

    def test_mais_producao_para_mesma_energia_reduz_sec(self):
        SEC_baixa_producao = consumo_especifico_energia(5000.0, 500.0)
        SEC_alta_producao = consumo_especifico_energia(5000.0, 2000.0)
        assert SEC_alta_producao < SEC_baixa_producao
