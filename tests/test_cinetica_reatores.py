import math

import pytest

from calculos_processo.cinetica_reatores import (
    constante_velocidade_arrhenius,
    conversao_cstr_primeira_ordem,
    conversao_pfr_primeira_ordem,
    numero_damkohler,
    taxa_reacao_ordem_n,
    tempo_batelada,
    tempo_espacial_cstr,
    tempo_espacial_pfr,
)


class TestArrhenius:
    def test_k_cresce_com_temperatura(self):
        k_frio = constante_velocidade_arrhenius(A=1e10, Ea=80000.0, T=300.0)
        k_quente = constante_velocidade_arrhenius(A=1e10, Ea=80000.0, T=340.0)
        assert k_quente > k_frio > 0


class TestTaxaReacao:
    def test_ordem_um(self):
        assert taxa_reacao_ordem_n(k=0.5, C=2.0, ordem=1) == pytest.approx(1.0)

    def test_ordem_dois(self):
        assert taxa_reacao_ordem_n(k=0.5, C=2.0, ordem=2) == pytest.approx(2.0)


class TestBatelada:
    def test_ordem_zero(self):
        assert tempo_batelada(k=0.5, CA0=10.0, CA=8.0, ordem=0) == pytest.approx(4.0)

    def test_ordem_um(self):
        assert tempo_batelada(k=0.1, CA0=2.0, CA=1.0, ordem=1) == pytest.approx(math.log(2.0) / 0.1)

    def test_ordem_dois(self):
        assert tempo_batelada(k=0.2, CA0=2.0, CA=1.0, ordem=2) == pytest.approx((1 / 1.0 - 1 / 2.0) / 0.2)

    def test_ordem_nao_suportada(self):
        with pytest.raises(NotImplementedError):
            tempo_batelada(k=0.1, CA0=2.0, CA=1.0, ordem=1.5)


class TestReatoresContinuos:
    def test_pfr_precisa_de_menos_tempo_espacial_que_cstr_mesma_conversao(self):
        # Para cinetica de ordem positiva, PFR e sempre mais eficiente que CSTR (mesma X).
        for ordem in (0, 1, 2):
            tau_cstr = tempo_espacial_cstr(k=0.2, CA0=2.0, X=0.6, ordem=ordem)
            tau_pfr = tempo_espacial_pfr(k=0.2, CA0=2.0, X=0.6, ordem=ordem)
            assert tau_pfr <= tau_cstr

    def test_conversao_cstr_e_inversa_de_tau_cstr_ordem_um(self):
        tau = tempo_espacial_cstr(k=0.1, CA0=2.0, X=0.5, ordem=1)
        assert conversao_cstr_primeira_ordem(k=0.1, tau=tau) == pytest.approx(0.5)

    def test_conversao_pfr_e_inversa_de_tau_pfr_ordem_um(self):
        tau = tempo_espacial_pfr(k=0.1, CA0=2.0, X=0.5, ordem=1)
        assert conversao_pfr_primeira_ordem(k=0.1, tau=tau) == pytest.approx(0.5)

    def test_conversao_cresce_com_tau(self):
        X_curto = conversao_pfr_primeira_ordem(k=0.1, tau=1.0)
        X_longo = conversao_pfr_primeira_ordem(k=0.1, tau=10.0)
        assert X_longo > X_curto


class TestDamkohler:
    def test_da_grande_para_reacao_rapida_ou_tau_grande(self):
        Da_baixo = numero_damkohler(k=0.01, tau=1.0, CA0=1.0, ordem=1)
        Da_alto = numero_damkohler(k=0.01, tau=1000.0, CA0=1.0, ordem=1)
        assert Da_alto > Da_baixo
