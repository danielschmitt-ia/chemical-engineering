import pytest

from calculos_processo.engenharia_particulas import diametro_medio_aritmetico, diametro_medio_sauter


class TestDiametroMedio:
    def test_populacao_monodispersa_os_dois_criterios_coincidem(self):
        # todas as particulas do mesmo tamanho -> D10 == D32 == esse tamanho
        D10 = diametro_medio_aritmetico([25.0], [100])
        D32 = diametro_medio_sauter([25.0], [100])
        assert D10 == pytest.approx(25.0)
        assert D32 == pytest.approx(25.0)

    def test_sauter_da_mais_peso_a_particulas_grandes_que_aritmetico(self):
        diametros = [10.0, 20.0, 30.0]
        quantidades = [100, 50, 10]
        D10 = diametro_medio_aritmetico(diametros, quantidades)
        D32 = diametro_medio_sauter(diametros, quantidades)
        assert D32 > D10

    def test_formula_direta_aritmetico(self):
        D10 = diametro_medio_aritmetico([10.0, 20.0], [1, 1])
        assert D10 == pytest.approx(15.0)
