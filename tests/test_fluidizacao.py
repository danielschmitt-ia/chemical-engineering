import pytest

from calculos_processo.fluidizacao import (
    numero_arquimedes,
    queda_pressao_leito_fluidizado,
    velocidade_minima_fluidizacao,
)


class TestArquimedes:
    def test_positivo_para_particula_mais_densa_que_fluido(self):
        Ar = numero_arquimedes(dp=200e-6, rho_particula=2600.0, rho_fluido=1.2, mu=1.8e-5)
        assert Ar > 0


class TestVelocidadeMinimaFluidizacao:
    def test_ordem_de_grandeza_areia_fina_em_ar(self):
        # Exemplo classico de didatica de fluidizacao: areia ~200 micron em ar, vmf tipicamente
        # da ordem de alguns cm/s.
        vmf = velocidade_minima_fluidizacao(dp=200e-6, rho_particula=2600.0, rho_fluido=1.2, mu=1.8e-5)
        assert 0.005 < vmf < 0.1

    def test_particula_maior_exige_velocidade_maior(self):
        vmf_fina = velocidade_minima_fluidizacao(dp=100e-6, rho_particula=2600.0, rho_fluido=1.2, mu=1.8e-5)
        vmf_grossa = velocidade_minima_fluidizacao(dp=500e-6, rho_particula=2600.0, rho_fluido=1.2, mu=1.8e-5)
        assert vmf_grossa > vmf_fina

    def test_particula_mais_densa_exige_velocidade_maior(self):
        vmf_leve = velocidade_minima_fluidizacao(dp=200e-6, rho_particula=1500.0, rho_fluido=1.2, mu=1.8e-5)
        vmf_densa = velocidade_minima_fluidizacao(dp=200e-6, rho_particula=2600.0, rho_fluido=1.2, mu=1.8e-5)
        assert vmf_densa > vmf_leve


class TestQuedaPressaoLeitoFluidizado:
    def test_proporcional_a_altura(self):
        dP1 = queda_pressao_leito_fluidizado(altura_leito=1.0, epsilon=0.5, rho_particula=2600.0, rho_fluido=1.2)
        dP2 = queda_pressao_leito_fluidizado(altura_leito=2.0, epsilon=0.5, rho_particula=2600.0, rho_fluido=1.2)
        assert dP2 == pytest.approx(2 * dP1)

    def test_independente_da_velocidade_por_definicao(self):
        # A funcao nao recebe velocidade -- reforca que dP do leito fluidizado (regime ja
        # fluidizado) so depende do peso do leito, nao da velocidade acima de vmf.
        dP = queda_pressao_leito_fluidizado(altura_leito=1.5, epsilon=0.45, rho_particula=2600.0, rho_fluido=1.2)
        assert dP > 0
