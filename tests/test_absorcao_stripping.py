import pytest

from calculos_processo.absorcao_stripping import (
    estagios_necessarios_absorcao,
    fator_absorcao,
    fator_esgotamento,
    fracao_nao_absorvida,
    fracao_nao_esgotada,
)


class TestFatores:
    def test_fator_absorcao(self):
        assert fator_absorcao(L=1000.0, m=0.8, G=900.0) == pytest.approx(1000.0 / (0.8 * 900.0))

    def test_fator_esgotamento_e_inverso_do_fator_absorcao_trocando_papeis(self):
        # fator_esgotamento(G, m, L) = m*G/L = 1/fator_absorcao(L, m, G)
        A = fator_absorcao(L=1000.0, m=0.8, G=900.0)
        S = fator_esgotamento(G=900.0, m=0.8, L=1000.0)
        assert S == pytest.approx(1.0 / A)


class TestAbsorcao:
    def test_mais_estagios_absorve_mais(self):
        phi_poucos = fracao_nao_absorvida(1000.0, 0.8, 900.0, N=2)
        phi_muitos = fracao_nao_absorvida(1000.0, 0.8, 900.0, N=10)
        assert phi_muitos < phi_poucos

    def test_estagios_necessarios_recupera_N(self):
        phi = fracao_nao_absorvida(1000.0, 0.8, 900.0, N=6)
        assert estagios_necessarios_absorcao(1000.0, 0.8, 900.0, phi) == pytest.approx(6.0)


class TestEsgotamento:
    def test_mais_estagios_esgota_mais(self):
        phi_poucos = fracao_nao_esgotada(900.0, 0.8, 1000.0, N=2)
        phi_muitos = fracao_nao_esgotada(900.0, 0.8, 1000.0, N=10)
        assert phi_muitos < phi_poucos
