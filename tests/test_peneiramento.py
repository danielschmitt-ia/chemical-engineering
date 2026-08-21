import pytest

from calculos_processo.peneiramento import eficiencia_peneiramento


class TestEficienciaPeneiramento:
    def test_formula_direta(self):
        E = eficiencia_peneiramento(massa_passante=450.0, fracao_fino_passante=0.95,
                                     massa_alimentacao=1000.0, fracao_fino_alimentacao=0.45)
        assert E == pytest.approx((450.0 * 0.95) / (1000.0 * 0.45))

    def test_peneira_ideal_eficiencia_um(self):
        # Toda a alimentacao fina (450 kg) passa integralmente, nada fica retido
        E = eficiencia_peneiramento(massa_passante=450.0, fracao_fino_passante=1.0,
                                     massa_alimentacao=1000.0, fracao_fino_alimentacao=0.45)
        assert E == pytest.approx(1.0)
