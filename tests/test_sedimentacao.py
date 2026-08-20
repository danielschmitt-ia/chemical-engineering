import pytest

from calculos_processo.sedimentacao import fluxo_massico_solidos, velocidade_sedimentacao_dificultada


class TestSedimentacaoDificultada:
    def test_diluicao_infinita_recupera_stokes(self):
        assert velocidade_sedimentacao_dificultada(v_stokes=0.002, epsilon=1.0) == pytest.approx(0.002)

    def test_mais_concentrado_sedimenta_mais_devagar(self):
        v_diluido = velocidade_sedimentacao_dificultada(0.002, epsilon=0.95)
        v_concentrado = velocidade_sedimentacao_dificultada(0.002, epsilon=0.5)
        assert v_concentrado < v_diluido

    def test_formula_direta(self):
        v = velocidade_sedimentacao_dificultada(0.002, epsilon=0.8, n=4.65)
        assert v == pytest.approx(0.002 * 0.8 ** 4.65)


class TestFluxoSolidos:
    def test_formula_direta(self):
        assert fluxo_massico_solidos(concentracao_solidos=50.0, velocidade_sedimentacao=0.002) == pytest.approx(0.1)
