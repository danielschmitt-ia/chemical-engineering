import pytest

from calculos_processo.mecanica_fluidos import (
    numero_reynolds_particula,
    potencia_eixo_bomba,
    potencia_hidraulica_bomba,
    trabalho_bomba_necessario,
    velocidade_terminal_stokes,
)


class TestTrabalhoBomba:
    def test_somente_elevacao_e_perdas(self):
        w = trabalho_bomba_necessario(P_entrada=101325.0, P_saida=101325.0, rho=1000.0,
                                       z_entrada=0.0, z_saida=30.0, perdas=50.0, g=9.81)
        assert w == pytest.approx(9.81 * 30 + 50.0)

    def test_variacao_de_pressao(self):
        w = trabalho_bomba_necessario(P_entrada=100000.0, P_saida=600000.0, rho=1000.0)
        assert w == pytest.approx(500.0)

    def test_sem_variacao_nenhuma_trabalho_e_zero(self):
        w = trabalho_bomba_necessario(P_entrada=100000.0, P_saida=100000.0, rho=1000.0)
        assert w == pytest.approx(0.0)


class TestPotenciaBomba:
    def test_potencia_hidraulica(self):
        P = potencia_hidraulica_bomba(vazao_volumetrica=0.02, altura_manometrica=25.0, rho=1000.0)
        assert P == pytest.approx(1000.0 * 0.02 * 9.81 * 25.0)

    def test_potencia_eixo_maior_que_hidraulica(self):
        Ph = potencia_hidraulica_bomba(0.02, 25.0, 1000.0)
        Pe = potencia_eixo_bomba(Ph, eficiencia=0.65)
        assert Pe > Ph

    def test_eficiencia_invalida(self):
        with pytest.raises(ValueError):
            potencia_eixo_bomba(1000.0, eficiencia=1.5)
        with pytest.raises(ValueError):
            potencia_eixo_bomba(1000.0, eficiencia=0.0)


class TestSedimentacao:
    def test_particula_mais_densa_sedimenta_mais_rapido(self):
        vt_leve = velocidade_terminal_stokes(50e-6, 1500.0, 1000.0, 1e-3)
        vt_densa = velocidade_terminal_stokes(50e-6, 2650.0, 1000.0, 1e-3)
        assert vt_densa > vt_leve > 0

    def test_particula_maior_sedimenta_mais_rapido(self):
        vt_pequena = velocidade_terminal_stokes(20e-6, 2650.0, 1000.0, 1e-3)
        vt_grande = velocidade_terminal_stokes(80e-6, 2650.0, 1000.0, 1e-3)
        assert vt_grande > vt_pequena

    def test_reynolds_particula_fina_e_regime_de_stokes(self):
        vt = velocidade_terminal_stokes(50e-6, 2650.0, 1000.0, 1e-3)
        Re = numero_reynolds_particula(1000.0, vt, 50e-6, 1e-3)
        assert Re < 1.0
