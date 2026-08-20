import pytest

from calculos_processo.filtragem import taxa_filtracao, tempo_filtracao_pressao_constante


class TestFiltragem:
    def test_formula_direta(self):
        t = tempo_filtracao_pressao_constante(V=0.01, alpha=1e11, Cs=50.0, Rm=1e10, mu=1e-3,
                                               delta_P=2e5, A=0.5)
        termo1 = (1e-3 * 1e11 * 50.0) / (2.0 * 2e5 * 0.5 ** 2) * 0.01 ** 2
        termo2 = (1e-3 * 1e10) / (2e5 * 0.5) * 0.01
        assert t == pytest.approx(termo1 + termo2)

    def test_mais_volume_demora_mais(self):
        t_pouco = tempo_filtracao_pressao_constante(0.005, 1e11, 50.0, 1e10, 1e-3, 2e5, 0.5)
        t_muito = tempo_filtracao_pressao_constante(0.02, 1e11, 50.0, 1e10, 1e-3, 2e5, 0.5)
        assert t_muito > t_pouco

    def test_taxa_cai_com_volume_acumulado(self):
        taxa_inicio = taxa_filtracao(V=0.001, alpha=1e11, Cs=50.0, Rm=1e10, mu=1e-3, delta_P=2e5, A=0.5)
        taxa_fim = taxa_filtracao(V=0.05, alpha=1e11, Cs=50.0, Rm=1e10, mu=1e-3, delta_P=2e5, A=0.5)
        assert taxa_fim < taxa_inicio
