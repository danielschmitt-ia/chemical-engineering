import pytest

from calculos_processo.analise_variabilidade import coeficiente_variacao, desvio_padrao_amostral


class TestDesvioPadrao:
    def test_formula_direta(self):
        s = desvio_padrao_amostral([10, 12, 11, 9, 13])
        media = 11.0
        variancia = sum((x - media) ** 2 for x in [10, 12, 11, 9, 13]) / 4
        assert s == pytest.approx(variancia ** 0.5)

    def test_sem_variacao_e_zero(self):
        assert desvio_padrao_amostral([5, 5, 5, 5]) == pytest.approx(0.0)


class TestCoeficienteVariacao:
    def test_formula_direta(self):
        assert coeficiente_variacao(desvio_padrao=2.0, media=10.0) == pytest.approx(0.2)
