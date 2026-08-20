import pytest

from calculos_processo.reologia import (
    fator_atrito_laminar_lei_potencia,
    reynolds_generalizado_lei_potencia,
    tensao_cisalhante_bingham,
    tensao_cisalhante_lei_potencia,
    viscosidade_aparente_lei_potencia,
)


class TestLeiDePotencia:
    def test_n_igual_um_e_fluido_newtoniano(self):
        # Para n=1, K faz o papel da viscosidade newtoniana: tau = K*gamma_dot
        assert tensao_cisalhante_lei_potencia(K=0.5, taxa_deformacao=10.0, n=1.0) == pytest.approx(5.0)

    def test_pseudoplastico_viscosidade_aparente_cai_com_taxa(self):
        mu_baixa_taxa = viscosidade_aparente_lei_potencia(K=2.0, taxa_deformacao=1.0, n=0.5)
        mu_alta_taxa = viscosidade_aparente_lei_potencia(K=2.0, taxa_deformacao=100.0, n=0.5)
        assert mu_alta_taxa < mu_baixa_taxa

    def test_dilatante_viscosidade_aparente_cresce_com_taxa(self):
        mu_baixa_taxa = viscosidade_aparente_lei_potencia(K=2.0, taxa_deformacao=1.0, n=1.5)
        mu_alta_taxa = viscosidade_aparente_lei_potencia(K=2.0, taxa_deformacao=100.0, n=1.5)
        assert mu_alta_taxa > mu_baixa_taxa


class TestBingham:
    def test_tensao_de_escoamento_desloca_a_reta(self):
        tau_sem_escoamento = tensao_cisalhante_bingham(tau0=0.0, mu_plastico=0.1, taxa_deformacao=5.0)
        tau_com_escoamento = tensao_cisalhante_bingham(tau0=10.0, mu_plastico=0.1, taxa_deformacao=5.0)
        assert tau_com_escoamento == pytest.approx(tau_sem_escoamento + 10.0)


class TestReynoldsGeneralizado:
    def test_n_igual_um_recupera_reynolds_newtoniano(self):
        rho, v, D, mu = 1000.0, 1.0, 0.05, 1e-3
        Re_newtoniano = rho * v * D / mu
        Re_generalizado = reynolds_generalizado_lei_potencia(rho, v, D, K=mu, n=1.0)
        assert Re_generalizado == pytest.approx(Re_newtoniano)

    def test_fator_atrito_laminar_e_64_sobre_re(self):
        assert fator_atrito_laminar_lei_potencia(800.0) == pytest.approx(64.0 / 800.0)
