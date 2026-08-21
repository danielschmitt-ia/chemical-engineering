import pytest

from calculos_processo.transferencia_calor import (
    area_troca_termica,
    calor_sensivel,
    coeficiente_global_troca,
    diferenca_temperatura_media_log,
    dtml_trocador,
    taxa_calor_trocador,
)


class TestCalorSensivel:
    def test_calculo_basico(self):
        assert calor_sensivel(vazao_massica=2.0, cp=4184.0, delta_T=10.0) == pytest.approx(83680.0)

    def test_sinal_negativo_quando_resfria(self):
        assert calor_sensivel(vazao_massica=2.0, cp=4184.0, delta_T=-10.0) < 0


class TestCoeficienteGlobal:
    def test_parede_ideal_e_media_harmonica_dos_filmes(self):
        U = coeficiente_global_troca(h_quente=1000.0, h_frio=1000.0)
        assert U == pytest.approx(500.0)

    def test_resistencia_de_parede_reduz_u(self):
        U_sem_parede = coeficiente_global_troca(h_quente=1000.0, h_frio=1000.0)
        U_com_parede = coeficiente_global_troca(h_quente=1000.0, h_frio=1000.0,
                                                  espessura_parede=0.005, k_parede=15.0)
        assert U_com_parede < U_sem_parede

    def test_incrustacao_reduz_u(self):
        U_limpo = coeficiente_global_troca(h_quente=1000.0, h_frio=1000.0)
        U_incrustado = coeficiente_global_troca(h_quente=1000.0, h_frio=1000.0,
                                                  resistencia_incrustacao_quente=1e-4)
        assert U_incrustado < U_limpo

    def test_espessura_sem_k_parede_levanta_erro(self):
        with pytest.raises(ValueError):
            coeficiente_global_troca(h_quente=1000.0, h_frio=1000.0, espessura_parede=0.005)


class TestDTML:
    def test_deltas_iguais_retorna_o_proprio_delta(self):
        assert diferenca_temperatura_media_log(20.0, 20.0) == pytest.approx(20.0)

    def test_formula_padrao(self):
        import math
        assert diferenca_temperatura_media_log(50.0, 10.0) == pytest.approx(40.0 / math.log(5.0))

    def test_rejeita_delta_nao_positivo(self):
        with pytest.raises(ValueError):
            diferenca_temperatura_media_log(-5.0, 10.0)

    def test_contracorrente_maior_ou_igual_a_cocorrente(self):
        # Para as mesmas 4 temperaturas terminais, contracorrente é sempre >= cocorrente.
        dtml_cc = dtml_trocador(T_quente_entrada=150.0, T_quente_saida=90.0,
                                 T_frio_entrada=30.0, T_frio_saida=80.0, arranjo="contracorrente")
        dtml_co = dtml_trocador(T_quente_entrada=150.0, T_quente_saida=90.0,
                                 T_frio_entrada=30.0, T_frio_saida=80.0, arranjo="cocorrente")
        assert dtml_cc >= dtml_co

    def test_arranjo_invalido(self):
        with pytest.raises(ValueError):
            dtml_trocador(100.0, 80.0, 30.0, 60.0, arranjo="cruzado")


class TestDimensionamento:
    def test_area_e_inversa_de_taxa_calor(self):
        U, dtml = 500.0, 25.0
        A = area_troca_termica(Q=100000.0, U=U, dtml=dtml)
        assert taxa_calor_trocador(U, A, dtml) == pytest.approx(100000.0)
