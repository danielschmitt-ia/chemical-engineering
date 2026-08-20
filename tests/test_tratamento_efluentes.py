import pytest

from calculos_processo.tratamento_efluentes import carga_poluente, eficiencia_remocao


class TestEficienciaRemocao:
    def test_formula_direta(self):
        assert eficiencia_remocao(concentracao_entrada=200.0, concentracao_saida=20.0) == pytest.approx(0.9)

    def test_sem_remocao_e_zero(self):
        assert eficiencia_remocao(200.0, 200.0) == pytest.approx(0.0)


class TestCargaPoluente:
    def test_formula_direta(self):
        assert carga_poluente(vazao=10.0, concentracao=200.0) == pytest.approx(2000.0)
