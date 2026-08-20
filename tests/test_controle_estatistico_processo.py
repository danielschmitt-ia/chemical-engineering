import math

import pytest

from calculos_processo.controle_estatistico_processo import (
    indice_capacidade_cp,
    indice_capacidade_cpk,
    limite_controle_inferior,
    limite_controle_superior,
)


class TestLimitesControle:
    def test_ucl_lcl_simetricos_em_torno_da_media(self):
        UCL = limite_controle_superior(100.0, 5.0)
        LCL = limite_controle_inferior(100.0, 5.0)
        assert UCL == pytest.approx(115.0)
        assert LCL == pytest.approx(85.0)
        assert (UCL + LCL) / 2 == pytest.approx(100.0)

    def test_subgrupo_maior_estreita_os_limites(self):
        UCL_individual = limite_controle_superior(100.0, 5.0, n_amostra=1)
        UCL_subgrupo = limite_controle_superior(100.0, 5.0, n_amostra=4)
        assert UCL_subgrupo < UCL_individual
        assert UCL_subgrupo == pytest.approx(100.0 + 3.0 * 5.0 / math.sqrt(4))


class TestCapacidade:
    def test_cp_formula_direta(self):
        assert indice_capacidade_cp(120.0, 80.0, 5.0) == pytest.approx(40.0 / 30.0)

    def test_cpk_processo_centrado_igual_a_cp(self):
        Cp = indice_capacidade_cp(120.0, 80.0, 5.0)
        Cpk = indice_capacidade_cpk(media=100.0, limite_superior_especificacao=120.0,
                                     limite_inferior_especificacao=80.0, desvio_padrao=5.0)
        assert Cpk == pytest.approx(Cp)

    def test_cpk_processo_descentrado_e_menor_que_cp(self):
        Cp = indice_capacidade_cp(120.0, 80.0, 5.0)
        Cpk = indice_capacidade_cpk(media=110.0, limite_superior_especificacao=120.0,
                                     limite_inferior_especificacao=80.0, desvio_padrao=5.0)
        assert Cpk < Cp
