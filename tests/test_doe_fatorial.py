import pytest

from calculos_processo.doe_fatorial import efeito_principal, numero_ensaios_fatorial


class TestNumeroEnsaios:
    def test_fatorial_completo_dois_niveis(self):
        assert numero_ensaios_fatorial(k=3) == 8

    def test_com_replicas(self):
        assert numero_ensaios_fatorial(k=3, replicas=2) == 16

    def test_tres_niveis(self):
        assert numero_ensaios_fatorial(k=2, niveis=3) == 9


class TestEfeitoPrincipal:
    def test_formula_direta(self):
        efeito = efeito_principal(respostas_nivel_alto=[10, 12, 11], respostas_nivel_baixo=[5, 6, 4])
        assert efeito == pytest.approx(11.0 - 5.0)

    def test_fator_sem_efeito_da_zero(self):
        efeito = efeito_principal([10, 10, 10], [10, 10, 10])
        assert efeito == pytest.approx(0.0)
