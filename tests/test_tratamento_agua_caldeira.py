import pytest

from calculos_processo.tratamento_agua_caldeira import ciclos_concentracao, vazao_purga


class TestCiclosConcentracao:
    def test_formula_direta(self):
        assert ciclos_concentracao(concentracao_purga=1500.0, concentracao_agua_alimentacao=100.0) == pytest.approx(15.0)


class TestVazaoPurga:
    def test_formula_direta(self):
        assert vazao_purga(vazao_vapor=10000.0, coc=15.0) == pytest.approx(10000.0 / 14.0)

    def test_coc_maior_reduz_purga(self):
        purga_coc_baixo = vazao_purga(10000.0, coc=5.0)
        purga_coc_alto = vazao_purga(10000.0, coc=20.0)
        assert purga_coc_alto < purga_coc_baixo

    def test_coc_menor_ou_igual_a_um_e_invalido(self):
        with pytest.raises(ValueError):
            vazao_purga(10000.0, coc=1.0)
