import pytest

from calculos_processo.mistura_agitacao import (
    numero_froude_agitacao,
    numero_reynolds_agitacao,
    potencia_agitador,
)


class TestReynolds:
    def test_formula_direta(self):
        assert numero_reynolds_agitacao(rho=1000.0, N=2.0, D=0.3, mu=1e-3) == pytest.approx(1000.0 * 2.0 * 0.3 ** 2 / 1e-3)


class TestFroude:
    def test_formula_direta(self):
        assert numero_froude_agitacao(N=2.0, D=0.3) == pytest.approx(2.0 ** 2 * 0.3 / 9.81)


class TestPotencia:
    def test_formula_direta(self):
        assert potencia_agitador(Po=5.0, rho=1000.0, N=2.0, D=0.3) == pytest.approx(5.0 * 1000.0 * 2.0 ** 3 * 0.3 ** 5)

    def test_potencia_cresce_forte_com_velocidade(self):
        # P ~ N^3: dobrar N deve multiplicar a potencia por 8
        P1 = potencia_agitador(1.0, 1000.0, 1.0, 0.3)
        P2 = potencia_agitador(1.0, 1000.0, 2.0, 0.3)
        assert P2 == pytest.approx(8 * P1)
