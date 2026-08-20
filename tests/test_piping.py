import math

import pytest

from calculos_processo.piping import (
    diametro_a_partir_de_velocidade,
    dilatacao_termica_tubulacao,
    espessura_minima_parede,
    tensao_admissivel_expansao_termica,
)


class TestDiametroPorVelocidade:
    def test_area_e_vazao_consistentes(self):
        D = diametro_a_partir_de_velocidade(vazao_volumetrica=0.01, velocidade_recomendada=2.0)
        area = math.pi * D ** 2 / 4
        assert area * 2.0 == pytest.approx(0.01)

    def test_velocidade_maior_exige_diametro_menor(self):
        D_lento = diametro_a_partir_de_velocidade(0.01, 1.0)
        D_rapido = diametro_a_partir_de_velocidade(0.01, 4.0)
        assert D_rapido < D_lento


class TestEspessuraMinima:
    def test_pressao_maior_exige_parede_mais_espessa(self):
        t_baixa = espessura_minima_parede(P=0.5e6, D=0.114, S=138e6)
        t_alta = espessura_minima_parede(P=2.0e6, D=0.114, S=138e6)
        assert t_alta > t_baixa

    def test_sobreespessura_soma_diretamente(self):
        t_sem = espessura_minima_parede(P=1.0e6, D=0.114, S=138e6)
        t_com = espessura_minima_parede(P=1.0e6, D=0.114, S=138e6, sobreespessura=0.001)
        assert t_com == pytest.approx(t_sem + 0.001)

    def test_material_mais_resistente_exige_parede_mais_fina(self):
        t_material_fraco = espessura_minima_parede(P=1.0e6, D=0.114, S=100e6)
        t_material_forte = espessura_minima_parede(P=1.0e6, D=0.114, S=200e6)
        assert t_material_forte < t_material_fraco


class TestDilatacaoTermica:
    def test_dilatacao_aco_carbono_ordem_de_grandeza(self):
        # alfa aco carbono ~ 12e-6 1/K; 50 m de linha, DeltaT=100K -> ~60 mm
        delta_L = dilatacao_termica_tubulacao(comprimento=50.0, coeficiente_dilatacao=12e-6, delta_T=100.0)
        assert delta_L == pytest.approx(0.06, abs=0.005)

    def test_proporcional_ao_comprimento(self):
        d1 = dilatacao_termica_tubulacao(10.0, 12e-6, 100.0)
        d2 = dilatacao_termica_tubulacao(20.0, 12e-6, 100.0)
        assert d2 == pytest.approx(2 * d1)


class TestTensaoAdmissivelExpansao:
    def test_formula_direta(self):
        assert tensao_admissivel_expansao_termica(Sc=138e6, Sh=100e6, f=1.0) == pytest.approx(
            1.25 * 138e6 + 0.25 * 100e6)

    def test_fator_ciclico_reduz_admissivel(self):
        Sa_continuo = tensao_admissivel_expansao_termica(Sc=138e6, Sh=100e6, f=1.0)
        Sa_ciclico = tensao_admissivel_expansao_termica(Sc=138e6, Sh=100e6, f=0.8)
        assert Sa_ciclico < Sa_continuo
