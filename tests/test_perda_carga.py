import math

import pytest

from calculos_processo.perda_carga import (
    fator_atrito_darcy,
    numero_reynolds,
    perda_carga_distribuida,
    perda_carga_localizada,
    perda_carga_total,
    velocidade_escoamento,
)


class TestVelocidadeEscoamento:
    def test_velocidade_area_conhecida(self):
        # D = 2/sqrt(pi) m -> area = 1 m2, Q=3 m3/s -> v=3 m/s
        D = 2 / math.sqrt(math.pi)
        assert velocidade_escoamento(3.0, D) == pytest.approx(3.0, rel=1e-6)


class TestReynolds:
    def test_agua_em_tubo_tipico_e_turbulento(self):
        # agua: rho=1000 kg/m3, mu=1e-3 Pa.s, v=1 m/s, D=0.05 m -> Re=50000
        Re = numero_reynolds(rho=1000.0, v=1.0, D=0.05, mu=1e-3)
        assert Re == pytest.approx(50000.0)


class TestFatorAtrito:
    def test_laminar_e_64_sobre_re(self):
        assert fator_atrito_darcy(1000.0) == pytest.approx(64.0 / 1000.0)

    def test_turbulento_tubo_liso_ordem_de_grandeza(self):
        # Para Re=1e5, tubo liso, f de Darcy deve ficar por volta de 0.018-0.02
        f = fator_atrito_darcy(1e5, rugosidade_relativa=0.0)
        assert 0.015 < f < 0.025

    def test_rugosidade_maior_aumenta_atrito(self):
        f_liso = fator_atrito_darcy(1e5, rugosidade_relativa=0.0)
        f_rugoso = fator_atrito_darcy(1e5, rugosidade_relativa=0.01)
        assert f_rugoso > f_liso

    def test_reynolds_invalido(self):
        with pytest.raises(ValueError):
            fator_atrito_darcy(0.0)


class TestPerdaCarga:
    def test_perda_distribuida_proporcional_ao_comprimento(self):
        dp_curto = perda_carga_distribuida(f=0.02, L=10.0, D=0.05, rho=1000.0, v=1.0)
        dp_longo = perda_carga_distribuida(f=0.02, L=20.0, D=0.05, rho=1000.0, v=1.0)
        assert dp_longo == pytest.approx(2 * dp_curto)

    def test_perda_localizada_proporcional_a_k(self):
        dp = perda_carga_localizada(K_total=2.5, rho=1000.0, v=2.0)
        assert dp == pytest.approx(2.5 * 1000.0 * 2.0 ** 2 / 2)

    def test_perda_carga_total_soma_distribuida_e_localizada(self):
        resultado = perda_carga_total(vazao_volumetrica=0.01, D=0.1, L=50.0, rho=1000.0, mu=1e-3,
                                       rugosidade_absoluta=4.5e-5, K_total=3.0)
        assert resultado["delta_p_total"] == pytest.approx(
            resultado["delta_p_distribuida"] + resultado["delta_p_localizada"])
        assert resultado["delta_p_total"] > 0
        assert resultado["reynolds"] > 0

    def test_perda_carga_total_zero_sem_acessorios_e_maior_com_eles(self):
        base = perda_carga_total(vazao_volumetrica=0.01, D=0.1, L=50.0, rho=1000.0, mu=1e-3)
        com_acessorios = perda_carga_total(vazao_volumetrica=0.01, D=0.1, L=50.0, rho=1000.0, mu=1e-3, K_total=5.0)
        assert base["delta_p_localizada"] == pytest.approx(0.0)
        assert com_acessorios["delta_p_total"] > base["delta_p_total"]
