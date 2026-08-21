import pytest

from calculos_processo.evaporacao import (
    concentracao_final_evaporador,
    economia_vapor,
    vapor_gerado_evaporador,
)


class TestBalancoEvaporador:
    def test_concentracao_final(self):
        assert concentracao_final_evaporador(F=1000.0, xF=0.1, V=800.0) == pytest.approx(0.5)

    def test_inversas_consistentes(self):
        V = vapor_gerado_evaporador(F=1000.0, xF=0.1, xL=0.5)
        xL_recuperado = concentracao_final_evaporador(F=1000.0, xF=0.1, V=V)
        assert xL_recuperado == pytest.approx(0.5)


class TestEconomiaVapor:
    def test_formula_direta(self):
        assert economia_vapor(800.0, 900.0) == pytest.approx(800.0 / 900.0)

    def test_efeito_unico_tipico_menor_que_um(self):
        assert economia_vapor(850.0, 1000.0) < 1.0
