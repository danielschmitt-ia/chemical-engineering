import pytest

from calculos_processo.membranas import coeficiente_rejeicao, fluxo_permeado, seletividade_ideal


class TestFluxoPermeado:
    def test_formula_direta(self):
        J = fluxo_permeado(permeabilidade=1e-10, espessura=1e-4, forca_motriz=10e5)
        assert J == pytest.approx(1e-10 / 1e-4 * 10e5)

    def test_membrana_mais_espessa_reduz_fluxo(self):
        J_fina = fluxo_permeado(1e-10, 1e-4, 10e5)
        J_grossa = fluxo_permeado(1e-10, 5e-4, 10e5)
        assert J_grossa < J_fina


class TestSeletividade:
    def test_formula_direta(self):
        assert seletividade_ideal(2e-10, 1e-11) == pytest.approx(20.0)

    def test_permeabilidades_iguais_seletividade_um(self):
        assert seletividade_ideal(1e-10, 1e-10) == pytest.approx(1.0)


class TestRejeicao:
    def test_rejeicao_total(self):
        assert coeficiente_rejeicao(C_permeado=0.0, C_alimentacao=35.0) == pytest.approx(1.0)

    def test_sem_rejeicao(self):
        assert coeficiente_rejeicao(C_permeado=35.0, C_alimentacao=35.0) == pytest.approx(0.0)

    def test_rejeicao_parcial(self):
        assert coeficiente_rejeicao(C_permeado=0.5, C_alimentacao=35.0) == pytest.approx(1.0 - 0.5 / 35.0)
