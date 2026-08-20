import math

import pytest

from calculos_processo.moagem import energia_lei_bond, energia_lei_kick, energia_lei_rittinger


class TestKick:
    def test_formula_direta(self):
        assert energia_lei_kick(Kk=2.0, F=1000.0, P=100.0) == pytest.approx(2.0 * math.log(1000.0 / 100.0))

    def test_sem_reducao_energia_zero(self):
        assert energia_lei_kick(2.0, 1000.0, 1000.0) == pytest.approx(0.0)


class TestRittinger:
    def test_formula_direta(self):
        assert energia_lei_rittinger(Kr=5.0, F=1000.0, P=100.0) == pytest.approx(5.0 * (1 / 100.0 - 1 / 1000.0))


class TestBond:
    def test_formula_direta(self):
        E = energia_lei_bond(Wi=13.0, F80=10000.0, P80=100.0)
        assert E == pytest.approx(10.0 * 13.0 * (1 / math.sqrt(100.0) - 1 / math.sqrt(10000.0)))

    def test_moagem_mais_fina_consome_mais_energia(self):
        E_grosso = energia_lei_bond(13.0, 10000.0, 1000.0)
        E_fino = energia_lei_bond(13.0, 10000.0, 100.0)
        assert E_fino > E_grosso
