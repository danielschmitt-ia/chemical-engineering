import math

import pytest

from calculos_processo.confiabilidade_ram import (
    confiabilidade_exponencial,
    disponibilidade,
    mtbf,
    mttr,
    taxa_falha,
)


class TestMTBFMTTR:
    def test_mtbf_formula_direta(self):
        assert mtbf(tempo_total_operacao=8760.0, numero_falhas=2) == pytest.approx(4380.0)

    def test_mttr_formula_direta(self):
        assert mttr(tempo_total_reparo=20.0, numero_reparos=2) == pytest.approx(10.0)


class TestDisponibilidade:
    def test_formula_direta(self):
        A = disponibilidade(mtbf_valor=4380.0, mttr_valor=10.0)
        assert A == pytest.approx(4380.0 / 4390.0)

    def test_mttr_menor_aumenta_disponibilidade(self):
        A_reparo_rapido = disponibilidade(1000.0, 2.0)
        A_reparo_lento = disponibilidade(1000.0, 20.0)
        assert A_reparo_rapido > A_reparo_lento

    def test_disponibilidade_sempre_entre_zero_e_um(self):
        A = disponibilidade(100.0, 900.0)
        assert 0.0 < A < 1.0


class TestTaxaFalha:
    def test_e_inverso_do_mtbf(self):
        assert taxa_falha(4380.0) == pytest.approx(1.0 / 4380.0)


class TestConfiabilidadeExponencial:
    def test_no_instante_zero_e_um(self):
        assert confiabilidade_exponencial(t=0.0, mtbf_valor=1000.0) == pytest.approx(1.0)

    def test_no_mtbf_e_1_sobre_e(self):
        R = confiabilidade_exponencial(t=1000.0, mtbf_valor=1000.0)
        assert R == pytest.approx(1.0 / math.e)

    def test_decresce_com_o_tempo(self):
        R_cedo = confiabilidade_exponencial(100.0, 4380.0)
        R_tarde = confiabilidade_exponencial(2000.0, 4380.0)
        assert R_tarde < R_cedo
