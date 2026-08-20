import pytest

from calculos_processo.quimica_verde import economia_atomica


class TestEconomiaAtomica:
    def test_reacao_de_adicao_tem_economia_proxima_de_um(self):
        # A + H2 -> AH2 (hidrogenacao, todos os atomos dos reagentes vao para o produto)
        AE = economia_atomica(massa_molar_produto=102.0, coeficiente_produto=1,
                               massas_molares_reagentes=[100.0, 2.0], coeficientes_reagentes=[1, 1])
        assert AE == pytest.approx(1.0)

    def test_reacao_com_subproduto_pesado_tem_economia_baixa(self):
        # A-X + B-Y -> A-B + X-Y (substituicao dupla, com X-Y como subproduto pesado)
        AE = economia_atomica(massa_molar_produto=50.0, coeficiente_produto=1,
                               massas_molares_reagentes=[100.0, 100.0], coeficientes_reagentes=[1, 1])
        assert AE == pytest.approx(50.0 / 200.0)
        assert AE < 0.5
