import pytest

from calculos_processo.valvulas_controle import (
    caracteristica_igual_percentagem,
    caracteristica_linear,
    cv_necessario,
    vazao_valvula_controle,
)


class TestVazaoValvula:
    def test_formula_direta(self):
        assert vazao_valvula_controle(Cv=50.0, delta_P=25.0, densidade_relativa=1.0) == pytest.approx(250.0)

    def test_fluido_mais_denso_reduz_vazao(self):
        Q_agua = vazao_valvula_controle(50.0, 25.0, densidade_relativa=1.0)
        Q_denso = vazao_valvula_controle(50.0, 25.0, densidade_relativa=2.0)
        assert Q_denso < Q_agua

    def test_cv_e_inversa(self):
        Q = vazao_valvula_controle(Cv=50.0, delta_P=25.0, densidade_relativa=1.2)
        assert cv_necessario(Q, 25.0, 1.2) == pytest.approx(50.0)


class TestCaracteristicas:
    def test_linear_e_identidade(self):
        assert caracteristica_linear(0.3) == pytest.approx(0.3)
        assert caracteristica_linear(1.0) == pytest.approx(1.0)

    def test_igual_percentagem_extremos(self):
        assert caracteristica_igual_percentagem(1.0, rangeabilidade=50.0) == pytest.approx(1.0)
        assert caracteristica_igual_percentagem(0.0, rangeabilidade=50.0) == pytest.approx(1.0 / 50.0)

    def test_igual_percentagem_e_monotonica_crescente(self):
        f1 = caracteristica_igual_percentagem(0.3, 50.0)
        f2 = caracteristica_igual_percentagem(0.7, 50.0)
        assert f2 > f1
