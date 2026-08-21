import pytest

from calculos_processo.fta_arvore_falhas import probabilidade_porta_e, probabilidade_porta_ou


class TestPortaE:
    def test_formula_direta(self):
        assert probabilidade_porta_e([0.01, 0.02]) == pytest.approx(0.0002)

    def test_e_sempre_reduz_ou_mantem_a_probabilidade(self):
        p = probabilidade_porta_e([0.5, 0.5, 0.5])
        assert p <= 0.5

    def test_um_unico_evento(self):
        assert probabilidade_porta_e([0.3]) == pytest.approx(0.3)


class TestPortaOu:
    def test_formula_direta(self):
        assert probabilidade_porta_ou([0.1, 0.2]) == pytest.approx(1.0 - 0.9 * 0.8)

    def test_ou_sempre_aumenta_ou_mantem_a_probabilidade(self):
        p = probabilidade_porta_ou([0.1, 0.1, 0.1])
        assert p >= 0.1

    def test_um_unico_evento(self):
        assert probabilidade_porta_ou([0.3]) == pytest.approx(0.3)

    def test_redundancia_e_dual_de_e_e_ou(self):
        # Um sistema com 2 canais redundantes falha (P_falha_sistema) so se AMBOS falharem (E);
        # ele funciona se PELO MENOS UM canal funcionar (OU sobre as probabilidades de
        # funcionamento, nao de falha) -- dualidade classica de confiabilidade.
        p_falha_canal = 0.1
        p_funciona_canal = 1.0 - p_falha_canal
        p_falha_sistema = probabilidade_porta_e([p_falha_canal, p_falha_canal])
        p_funciona_sistema = probabilidade_porta_ou([p_funciona_canal, p_funciona_canal])
        assert p_falha_sistema == pytest.approx(1.0 - p_funciona_sistema)
