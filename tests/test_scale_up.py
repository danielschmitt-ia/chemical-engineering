import math

import pytest

from calculos_processo.scale_up import (
    escalonamento_lei_potencia,
    velocidade_escala_froude_constante,
    velocidade_escala_ponta_pa_constante,
    velocidade_escala_potencia_por_volume_constante,
    velocidade_escala_reynolds_constante,
)


class TestCriteriosMistura:
    def test_ponta_pa_constante(self):
        # v_ponta = pi*N*D constante -> N2 = N1*D1/D2
        assert velocidade_escala_ponta_pa_constante(N1=2.0, D1=0.3, D2=0.6) == pytest.approx(1.0)

    def test_potencia_por_volume_constante(self):
        assert velocidade_escala_potencia_por_volume_constante(2.0, 0.3, 0.6) == pytest.approx(2.0 * (0.5) ** (2 / 3))

    def test_reynolds_constante(self):
        assert velocidade_escala_reynolds_constante(2.0, 0.3, 0.6) == pytest.approx(2.0 * 0.25)

    def test_froude_constante(self):
        assert velocidade_escala_froude_constante(2.0, 0.3, 0.6) == pytest.approx(2.0 * math.sqrt(0.5))

    def test_criterios_concordam_quando_nao_ha_mudanca_de_escala(self):
        # D1 == D2 -> todos os criterios devem retornar N1 inalterado
        for func in (velocidade_escala_ponta_pa_constante, velocidade_escala_potencia_por_volume_constante,
                     velocidade_escala_reynolds_constante, velocidade_escala_froude_constante):
            assert func(5.0, 0.4, 0.4) == pytest.approx(5.0)


class TestEscalonamentoLeiPotencia:
    def test_formula_direta(self):
        assert escalonamento_lei_potencia(X1=10.0, S1=1.0, S2=8.0, expoente=2.0 / 3.0) == pytest.approx(10.0 * 8 ** (2 / 3))

    def test_scale_down_e_scale_up_consistentes(self):
        X_up = escalonamento_lei_potencia(X1=10.0, S1=1.0, S2=4.0, expoente=0.5)
        X_down = escalonamento_lei_potencia(X1=X_up, S1=4.0, S2=1.0, expoente=0.5)
        assert X_down == pytest.approx(10.0)

    def test_expoente_zero_nao_muda_nada(self):
        assert escalonamento_lei_potencia(X1=7.0, S1=1.0, S2=100.0, expoente=0.0) == pytest.approx(7.0)
