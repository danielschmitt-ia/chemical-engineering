import math

import pytest

from calculos_processo.hidrodinamica_colunas import (
    parametro_fluxo_fair,
    velocidade_inundacao_souders_brown,
)


class TestParametroFluxo:
    def test_formula_direta(self):
        FLV = parametro_fluxo_fair(L=5000.0, G=3000.0, rho_vapor=2.0, rho_liquido=800.0)
        assert FLV == pytest.approx((5000.0 / 3000.0) * math.sqrt(2.0 / 800.0))

    def test_mais_liquido_aumenta_flv(self):
        FLV_pouco = parametro_fluxo_fair(1000.0, 3000.0, 2.0, 800.0)
        FLV_muito = parametro_fluxo_fair(5000.0, 3000.0, 2.0, 800.0)
        assert FLV_muito > FLV_pouco


class TestVelocidadeInundacao:
    def test_formula_direta(self):
        v = velocidade_inundacao_souders_brown(C_sb=0.08, rho_liquido=800.0, rho_vapor=2.0)
        assert v == pytest.approx(0.08 * math.sqrt((800.0 - 2.0) / 2.0))

    def test_maior_c_sb_aumenta_velocidade_inundacao(self):
        v_baixo = velocidade_inundacao_souders_brown(0.05, 800.0, 2.0)
        v_alto = velocidade_inundacao_souders_brown(0.15, 800.0, 2.0)
        assert v_alto > v_baixo
