import pytest

from calculos_processo.destilacao import (
    composicao_liquido_equilibrio,
    equilibrio_binario,
    estagios_gilliland,
    estagios_mccabe_thiele,
    numero_minimo_estagios_fenske,
    refluxo_minimo,
    volatilidade_relativa,
)

# Caso de referência tipo benzeno/tolueno: alpha=2.5, xD=0.95, xB=0.05, xF=0.5, alimentação
# líquido saturado (q=1) — valores usados nos testes abaixo foram conferidos manualmente.
ALPHA = 2.5
XD, XB, XF = 0.95, 0.05, 0.5


class TestEquilibrioBinario:
    def test_volatilidade_relativa_de_pressoes_de_vapor(self):
        assert volatilidade_relativa(pressao_vapor_leve=250.0, pressao_vapor_pesado=100.0) == pytest.approx(2.5)

    def test_componente_puro_leve(self):
        assert equilibrio_binario(1.0, ALPHA) == pytest.approx(1.0)

    def test_componente_puro_pesado(self):
        assert equilibrio_binario(0.0, ALPHA) == pytest.approx(0.0)

    def test_alpha_maior_que_um_enriquece_o_vapor(self):
        assert equilibrio_binario(0.5, ALPHA) > 0.5

    def test_inversa_recupera_x(self):
        y = equilibrio_binario(0.3, ALPHA)
        assert composicao_liquido_equilibrio(y, ALPHA) == pytest.approx(0.3)


class TestFenske:
    def test_estagios_minimos_caso_referencia(self):
        Nmin = numero_minimo_estagios_fenske(XD, XB, ALPHA)
        assert Nmin == pytest.approx(6.427, abs=1e-3)

    def test_separacao_mais_dificil_exige_mais_estagios(self):
        Nmin_facil = numero_minimo_estagios_fenske(0.90, 0.10, ALPHA)
        Nmin_dificil = numero_minimo_estagios_fenske(0.99, 0.01, ALPHA)
        assert Nmin_dificil > Nmin_facil


class TestRefluxoMinimo:
    def test_caso_referencia_q_igual_um(self):
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        assert Rmin == pytest.approx(1.10, abs=1e-2)

    def test_alimentacao_bifasica_da_resultado_proximo_a_q_igual_um(self):
        # Para q levemente diferente de 1, o resultado deve continuar próximo (continuidade).
        Rmin_q1 = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        Rmin_q_quase_1 = refluxo_minimo(XD, XF, ALPHA, q=0.99)
        assert Rmin_q_quase_1 == pytest.approx(Rmin_q1, abs=0.05)


class TestGilliland:
    def test_converge_para_fenske_quando_r_tende_ao_infinito(self):
        Nmin = numero_minimo_estagios_fenske(XD, XB, ALPHA)
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        N_grande_reflexo = estagios_gilliland(Nmin, Rmin, R=1000 * Rmin)
        assert N_grande_reflexo == pytest.approx(Nmin, rel=1e-2)

    def test_estagios_reais_maior_que_estagios_minimos(self):
        Nmin = numero_minimo_estagios_fenske(XD, XB, ALPHA)
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        N = estagios_gilliland(Nmin, Rmin, R=2.2 * Rmin)
        assert N > Nmin

    def test_reflexo_abaixo_do_minimo_e_invalido(self):
        Nmin = numero_minimo_estagios_fenske(XD, XB, ALPHA)
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        with pytest.raises(ValueError):
            estagios_gilliland(Nmin, Rmin, R=Rmin * 0.9)


class TestMcCabeThiele:
    def test_numero_de_estagios_caso_referencia(self):
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        n, pontos = estagios_mccabe_thiele(XD, XB, XF, ALPHA, R=2.2 * Rmin, q=1.0)
        assert n == 10
        assert pontos[0] == (XD, XD)
        assert pontos[-1][0] <= XB

    def test_mais_refluxo_reduz_numero_de_estagios(self):
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        n_baixo, _ = estagios_mccabe_thiele(XD, XB, XF, ALPHA, R=1.5 * Rmin, q=1.0)
        n_alto, _ = estagios_mccabe_thiele(XD, XB, XF, ALPHA, R=4.0 * Rmin, q=1.0)
        assert n_alto < n_baixo

    def test_estagios_no_minimo_de_reflexo_e_proximo_de_fenske(self):
        # A refluxo bem alto (perto de total), o algébrico deve se aproximar do Fenske.
        Rmin = refluxo_minimo(XD, XF, ALPHA, q=1.0)
        Nmin = numero_minimo_estagios_fenske(XD, XB, ALPHA)
        n, _ = estagios_mccabe_thiele(XD, XB, XF, ALPHA, R=50 * Rmin, q=1.0)
        assert n == pytest.approx(Nmin, abs=1.0)

    def test_composicoes_fora_de_ordem_levantam_erro(self):
        with pytest.raises(ValueError):
            estagios_mccabe_thiele(xD=0.5, xB=0.6, xF=0.4, alpha=ALPHA, R=5.0)
