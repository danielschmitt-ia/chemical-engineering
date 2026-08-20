import pytest

from calculos_processo.fmea_rpn import numero_prioridade_risco


class TestRPN:
    def test_formula_direta(self):
        assert numero_prioridade_risco(severidade=8, ocorrencia=5, deteccao=3) == pytest.approx(120.0)

    def test_qualquer_fator_zero_da_rpn_zero(self):
        assert numero_prioridade_risco(severidade=0, ocorrencia=5, deteccao=3) == pytest.approx(0.0)

    def test_pior_caso_e_maximo(self):
        assert numero_prioridade_risco(10, 10, 10) == pytest.approx(1000.0)
