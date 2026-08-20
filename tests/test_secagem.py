import math

import pytest

from calculos_processo.secagem import (
    tempo_secagem_taxa_constante,
    tempo_secagem_taxa_decrescente,
    tempo_secagem_total,
)


class TestTaxaConstante:
    def test_formula_direta(self):
        t = tempo_secagem_taxa_constante(Ls=100.0, A=2.0, Rc=2.0, X1=0.5, Xc=0.2)
        assert t == pytest.approx(100.0 * (0.5 - 0.2) / (2.0 * 2.0))


class TestTaxaDecrescente:
    def test_formula_direta(self):
        t = tempo_secagem_taxa_decrescente(Ls=100.0, A=2.0, Rc=2.0, Xc=0.2, X2=0.05)
        assert t == pytest.approx((100.0 * 0.2) / (2.0 * 2.0) * math.log(0.2 / 0.05))


class TestTempoTotal:
    def test_soma_os_dois_periodos(self):
        t_total = tempo_secagem_total(Ls=100.0, A=2.0, Rc=2.0, X1=0.5, Xc=0.2, X2=0.05)
        t_c = tempo_secagem_taxa_constante(100.0, 2.0, 2.0, 0.5, 0.2)
        t_f = tempo_secagem_taxa_decrescente(100.0, 2.0, 2.0, 0.2, 0.05)
        assert t_total == pytest.approx(t_c + t_f)

    def test_sem_periodo_de_taxa_constante_se_ja_abaixo_da_critica(self):
        t_total = tempo_secagem_total(Ls=100.0, A=2.0, Rc=2.0, X1=0.15, Xc=0.2, X2=0.05)
        t_f = tempo_secagem_taxa_decrescente(100.0, 2.0, 2.0, 0.2, 0.05)
        assert t_total == pytest.approx(t_f)
