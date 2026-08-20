import pytest

from calculos_processo.manufatura_enxuta import disponibilidade_oee, oee, performance_oee, qualidade_oee


class TestComponentesOEE:
    def test_disponibilidade(self):
        assert disponibilidade_oee(450.0, 480.0) == pytest.approx(450.0 / 480.0)

    def test_performance(self):
        assert performance_oee(1000.0, 0.4, 450.0) == pytest.approx((1000.0 * 0.4) / 450.0)

    def test_qualidade(self):
        assert qualidade_oee(950.0, 1000.0) == pytest.approx(0.95)


class TestOEE:
    def test_e_o_produto_dos_tres_componentes(self):
        A, P, Q = 0.9, 0.85, 0.95
        assert oee(A, P, Q) == pytest.approx(A * P * Q)

    def test_perda_em_qualquer_componente_reduz_oee(self):
        oee_base = oee(1.0, 1.0, 1.0)
        oee_com_perda = oee(0.9, 1.0, 1.0)
        assert oee_com_perda < oee_base
