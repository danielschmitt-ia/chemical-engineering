import pytest

from calculos_processo.conversao import (
    conversao,
    grau_avanco,
    mols_a_partir_avanco,
    quantidade_final_a_partir_conversao,
    reagente_limitante,
    rendimento_a_partir_de_mols,
    rendimento_global,
    seletividade,
)


class TestConversao:
    def test_conversao_basica(self):
        assert conversao(100.0, 25.0) == pytest.approx(0.75)

    def test_conversao_total(self):
        assert conversao(100.0, 0.0) == pytest.approx(1.0)

    def test_conversao_nula(self):
        assert conversao(100.0, 100.0) == pytest.approx(0.0)

    def test_inversa_recupera_quantidade_final(self):
        X = conversao(80.0, 20.0)
        assert quantidade_final_a_partir_conversao(80.0, X) == pytest.approx(20.0)

    def test_quantidade_inicial_invalida(self):
        with pytest.raises(ValueError):
            conversao(0.0, 0.0)


class TestReagenteLimitante:
    def test_identifica_limitante_por_razao_estequiometrica(self):
        # A + 3B -> produtos; 10 mol de A e 20 mol de B: razao A=10, razao B=20/3=6.67 -> B limita
        assert reagente_limitante({"A": 10.0, "B": 20.0}, {"A": 1.0, "B": 3.0}) == "B"

    def test_maior_quantidade_em_mols_pode_nao_ser_limitante(self):
        # 100 mol de A (coef 1) vs 50 mol de B (coef 1): B tem menos mols e limita
        assert reagente_limitante({"A": 100.0, "B": 50.0}, {"A": 1.0, "B": 1.0}) == "B"

    def test_reagentes_inconsistentes(self):
        with pytest.raises(ValueError):
            reagente_limitante({"A": 10.0}, {"A": 1.0, "B": 1.0})


class TestGrauAvanco:
    def test_reagente_consumido_avanco_positivo(self):
        # A + 3B -> 2C; nu_A = -1; A cai de 10 para 6 mol
        assert grau_avanco(mols_inicial=10.0, mols_final=6.0, coeficiente_estequiometrico=-1.0) == pytest.approx(4.0)

    def test_produto_formado_mesmo_avanco(self):
        # nu_C = 2; C sobe de 0 para 8 mol -> mesmo xi=4 do reagente A acima
        assert grau_avanco(mols_inicial=0.0, mols_final=8.0, coeficiente_estequiometrico=2.0) == pytest.approx(4.0)

    def test_inversa_mols_a_partir_avanco(self):
        assert mols_a_partir_avanco(mols_inicial=10.0, coeficiente_estequiometrico=-1.0, avanco=4.0) == pytest.approx(6.0)

    def test_coeficiente_zero_invalido(self):
        with pytest.raises(ValueError):
            grau_avanco(10.0, 6.0, 0.0)


class TestSeletividadeRendimento:
    def test_seletividade_basica(self):
        assert seletividade(mols_produto_desejado=8.0, mols_produto_indesejado=2.0) == pytest.approx(4.0)

    def test_seletividade_perfeita_sem_subproduto(self):
        assert seletividade(mols_produto_desejado=8.0, mols_produto_indesejado=0.0) == float("inf")

    def test_seletividade_nenhum_produto_formado(self):
        assert seletividade(mols_produto_desejado=0.0, mols_produto_indesejado=0.0) == pytest.approx(0.0)

    def test_rendimento_global_e_produto_de_conversao_e_seletividade(self):
        assert rendimento_global(X=0.8, S=0.5) == pytest.approx(0.4)

    def test_rendimento_a_partir_de_mols(self):
        assert rendimento_a_partir_de_mols(mols_produto_obtido=30.0, mols_produto_teorico_maximo=50.0) == pytest.approx(0.6)
