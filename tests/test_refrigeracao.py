import pytest

from calculos_processo.refrigeracao import cop_carnot_bomba_calor, cop_carnot_refrigeracao, cop_refrigeracao


class TestCOPReal:
    def test_formula_direta(self):
        assert cop_refrigeracao(Q_evaporador=100.0, W_compressor=30.0) == pytest.approx(100.0 / 30.0)


class TestCOPCarnot:
    def test_formula_direta(self):
        COP = cop_carnot_refrigeracao(T_evaporador=263.15, T_condensador=313.15)
        assert COP == pytest.approx(263.15 / (313.15 - 263.15))

    def test_real_nunca_supera_carnot(self):
        # verificacao de consistencia fisica: um COP real razoavel deve ficar abaixo do limite
        # teorico de Carnot para as mesmas temperaturas
        COP_real = cop_refrigeracao(Q_evaporador=100.0, W_compressor=30.0)
        COP_carnot = cop_carnot_refrigeracao(T_evaporador=263.15, T_condensador=313.15)
        assert COP_real < COP_carnot

    def test_menor_diferenca_de_temperatura_aumenta_cop_maximo(self):
        COP_diferenca_grande = cop_carnot_refrigeracao(T_evaporador=250.0, T_condensador=320.0)
        COP_diferenca_pequena = cop_carnot_refrigeracao(T_evaporador=250.0, T_condensador=270.0)
        assert COP_diferenca_pequena > COP_diferenca_grande


class TestCOPBombaCalor:
    def test_bomba_calor_e_refrigeracao_mais_um(self):
        COP_refrig = cop_carnot_refrigeracao(T_evaporador=263.15, T_condensador=313.15)
        COP_bc = cop_carnot_bomba_calor(T_condensador=313.15, T_evaporador=263.15)
        assert COP_bc == pytest.approx(COP_refrig + 1.0)
