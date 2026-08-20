import numpy as np
import pytest

from calculos_processo.engenharia_alimentos import (
    letalidade_acumulada,
    populacao_sobrevivente,
    reducoes_logaritmicas,
    taxa_letal,
    valor_D_na_temperatura,
)


class TestTaxaLetal:
    def test_na_temperatura_de_referencia_e_um(self):
        assert taxa_letal(T=121.1, T_ref=121.1, z=10.0) == pytest.approx(1.0)

    def test_dez_graus_acima_multiplica_por_dez(self):
        assert taxa_letal(T=131.1, T_ref=121.1, z=10.0) == pytest.approx(10.0)

    def test_dez_graus_abaixo_divide_por_dez(self):
        assert taxa_letal(T=111.1, T_ref=121.1, z=10.0) == pytest.approx(0.1)


class TestValorD:
    def test_na_referencia_recupera_D_ref(self):
        assert valor_D_na_temperatura(D_ref=0.21, T=121.1, T_ref=121.1, z=10.0) == pytest.approx(0.21)

    def test_temperatura_maior_reduz_D(self):
        D_alta_T = valor_D_na_temperatura(D_ref=0.21, T=131.1, T_ref=121.1, z=10.0)
        assert D_alta_T == pytest.approx(0.021)


class TestLetalidadeAcumulada:
    def test_temperatura_constante_na_referencia_por_t_minutos(self):
        tempos = np.linspace(0.0, 5.0, 500)
        temperaturas = np.full_like(tempos, 121.1)
        F0 = letalidade_acumulada(tempos, temperaturas, T_ref=121.1, z=10.0)
        assert F0 == pytest.approx(5.0, rel=1e-3)

    def test_temperatura_abaixo_da_referencia_acumula_pouca_letalidade(self):
        tempos = np.linspace(0.0, 5.0, 500)
        temperaturas = np.full_like(tempos, 90.0)
        F0 = letalidade_acumulada(tempos, temperaturas, T_ref=121.1, z=10.0)
        assert F0 < 0.01


class TestReducoesEPopulacao:
    def test_reducoes_logaritmicas(self):
        assert reducoes_logaritmicas(F0=2.52, D_ref=0.21) == pytest.approx(12.0)

    def test_populacao_sobrevivente_apos_12D(self):
        assert populacao_sobrevivente(N0=1e6, reducoes_log=12.0) == pytest.approx(1e-6)

    def test_populacao_sobrevivente_zero_reducoes_mantem_populacao(self):
        assert populacao_sobrevivente(N0=1e6, reducoes_log=0.0) == pytest.approx(1e6)
