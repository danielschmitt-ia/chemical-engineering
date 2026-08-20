import pytest

from calculos_processo.reatores_leito_fixo import (
    fator_efetividade_esfera,
    modulo_thiele_esfera,
    queda_pressao_ergun,
)


class TestErgun:
    def test_queda_de_pressao_positiva(self):
        dP = queda_pressao_ergun(v=0.1, dp=0.005, epsilon=0.4, rho=1.2, mu=1.8e-5, L=1.0)
        assert dP > 0

    def test_proporcional_ao_comprimento(self):
        dP_curto = queda_pressao_ergun(v=0.1, dp=0.005, epsilon=0.4, rho=1.2, mu=1.8e-5, L=1.0)
        dP_longo = queda_pressao_ergun(v=0.1, dp=0.005, epsilon=0.4, rho=1.2, mu=1.8e-5, L=2.0)
        assert dP_longo == pytest.approx(2 * dP_curto)

    def test_leito_mais_compacto_aumenta_queda_de_pressao(self):
        dP_solto = queda_pressao_ergun(v=0.1, dp=0.005, epsilon=0.5, rho=1.2, mu=1.8e-5, L=1.0)
        dP_compacto = queda_pressao_ergun(v=0.1, dp=0.005, epsilon=0.3, rho=1.2, mu=1.8e-5, L=1.0)
        assert dP_compacto > dP_solto


class TestThiele:
    def test_particula_menor_reduz_modulo_thiele(self):
        phi_grande = modulo_thiele_esfera(raio_particula=5e-3, k=0.5, D_efetivo=1e-9)
        phi_pequeno = modulo_thiele_esfera(raio_particula=5e-4, k=0.5, D_efetivo=1e-9)
        assert phi_pequeno < phi_grande

    def test_efetividade_tende_a_um_para_phi_pequeno(self):
        assert fator_efetividade_esfera(1e-6) == pytest.approx(1.0, abs=1e-4)

    def test_efetividade_cai_com_phi_grande(self):
        eta_moderado = fator_efetividade_esfera(1.0)
        eta_grande = fator_efetividade_esfera(50.0)
        assert 0 < eta_grande < eta_moderado < 1.0

    def test_efetividade_grande_phi_aproxima_3_sobre_phi(self):
        phi = 100.0
        assert fator_efetividade_esfera(phi) == pytest.approx(3.0 / phi, rel=0.05)
