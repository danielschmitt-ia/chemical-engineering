import pytest

from calculos_processo.controle_pid import parametros_isa_para_paralelo, saida_pid_paralelo


class TestConversaoISA:
    def test_formula_direta(self):
        Kp, Ki, Kd = parametros_isa_para_paralelo(Kp=2.0, Ti=10.0, Td=1.0)
        assert (Kp, Ki, Kd) == pytest.approx((2.0, 0.2, 2.0))


class TestSaidaPID:
    def test_formula_direta(self):
        u = saida_pid_paralelo(Kp=2.0, Ki=0.2, Kd=2.0, erro=5.0, integral_erro=20.0,
                                erro_anterior=6.0, dt=1.0)
        assert u == pytest.approx(2.0 * 5.0 + 0.2 * 20.0 + 2.0 * (5.0 - 6.0) / 1.0)

    def test_so_proporcional_quando_ki_kd_zero(self):
        u = saida_pid_paralelo(Kp=3.0, Ki=0.0, Kd=0.0, erro=4.0, integral_erro=100.0,
                                erro_anterior=0.0, dt=1.0)
        assert u == pytest.approx(12.0)

    def test_erro_diminuindo_da_termo_derivativo_negativo(self):
        # erro caindo de 10 para 5: a variacao do erro e negativa, entao o termo derivativo
        # (que amortece a acao de controle) tambem e negativo
        u_com_derivativo = saida_pid_paralelo(Kp=1.0, Ki=0.0, Kd=1.0, erro=5.0, integral_erro=0.0,
                                               erro_anterior=10.0, dt=1.0)
        u_so_proporcional = saida_pid_paralelo(Kp=1.0, Ki=0.0, Kd=0.0, erro=5.0, integral_erro=0.0,
                                                erro_anterior=10.0, dt=1.0)
        assert u_com_derivativo < u_so_proporcional
