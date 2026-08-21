import pytest

from calculos_processo.eletroquimica import (
    eficiencia_corrente,
    massa_produzida_faraday,
    mols_produzidos_faraday,
    potencial_nernst,
    tempo_necessario_faraday,
)


class TestFaraday:
    def test_deposicao_de_cobre_1h_10A(self):
        # Cu2+ + 2e- -> Cu; M=63.5 g/mol; classico exemplo didatico de eletroquimica.
        m = massa_produzida_faraday(corrente=10.0, tempo=3600.0, massa_molar=63.5, n_eletrons=2)
        assert m == pytest.approx(11.85, abs=0.01)

    def test_mols_proporcional_a_corrente(self):
        n1 = mols_produzidos_faraday(corrente=5.0, tempo=1000.0, n_eletrons=1)
        n2 = mols_produzidos_faraday(corrente=10.0, tempo=1000.0, n_eletrons=1)
        assert n2 == pytest.approx(2 * n1)

    def test_tempo_necessario_e_inverso_de_massa_produzida(self):
        m = massa_produzida_faraday(corrente=10.0, tempo=1800.0, massa_molar=63.5, n_eletrons=2)
        t = tempo_necessario_faraday(massa_alvo=m, corrente=10.0, massa_molar=63.5, n_eletrons=2)
        assert t == pytest.approx(1800.0)

    def test_eficiencia_corrente(self):
        assert eficiencia_corrente(massa_real=9.0, massa_teorica=12.0) == pytest.approx(0.75)


class TestNernst:
    def test_quociente_reacao_um_recupera_potencial_padrao(self):
        assert potencial_nernst(E0=0.34, T=298.15, n_eletrons=2, Q=1.0) == pytest.approx(0.34)

    def test_quociente_maior_que_um_reduz_potencial(self):
        E = potencial_nernst(E0=0.34, T=298.15, n_eletrons=2, Q=10.0)
        assert E < 0.34
