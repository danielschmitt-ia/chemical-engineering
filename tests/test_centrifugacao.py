import math

import pytest

from calculos_processo.centrifugacao import forca_g_centrifuga, velocidade_sedimentacao_centrifuga
from calculos_processo.mecanica_fluidos import velocidade_terminal_stokes


class TestForcaG:
    def test_formula_direta(self):
        omega = 2 * math.pi * 1000 / 60
        g_force = forca_g_centrifuga(omega=omega, r=0.1)
        assert g_force == pytest.approx(omega ** 2 * 0.1 / 9.81)

    def test_mais_rotacao_aumenta_g_force(self):
        omega_baixo = 2 * math.pi * 500 / 60
        omega_alto = 2 * math.pi * 2000 / 60
        assert forca_g_centrifuga(omega_alto, 0.1) > forca_g_centrifuga(omega_baixo, 0.1)


class TestVelocidadeSedimentacaoCentrifuga:
    def test_razao_com_stokes_normal_e_o_g_force(self):
        omega = 2 * math.pi * 1000 / 60
        r = 0.1
        v_centrifuga = velocidade_sedimentacao_centrifuga(d_particula=1e-6, rho_particula=1200.0,
                                                            rho_fluido=1000.0, mu_fluido=1e-3,
                                                            omega=omega, r=r)
        v_gravidade = velocidade_terminal_stokes(d_particula=1e-6, rho_particula=1200.0,
                                                  rho_fluido=1000.0, mu_fluido=1e-3)
        g_force = forca_g_centrifuga(omega, r)
        assert v_centrifuga / v_gravidade == pytest.approx(g_force, rel=1e-9)
