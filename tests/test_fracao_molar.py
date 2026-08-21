import pytest

from calculos_processo.fracao_molar import (
    fracao_massica_a_partir_molar,
    fracao_molar_a_partir_massica,
    massa_molar_media,
    pressao_parcial,
)


class TestMassaMolarMedia:
    def test_componente_puro(self):
        assert massa_molar_media({"agua": 1.0}, {"agua": 18.015}) == pytest.approx(18.015)

    def test_mistura_binaria(self):
        # 50/50 molar entre M=18 e M=46 -> media = 32
        M = massa_molar_media({"agua": 0.5, "etanol": 0.5}, {"agua": 18.0, "etanol": 46.0})
        assert M == pytest.approx(32.0)

    def test_rejeita_fracoes_que_nao_somam_um(self):
        with pytest.raises(ValueError):
            massa_molar_media({"agua": 0.6, "etanol": 0.6}, {"agua": 18.0, "etanol": 46.0})


class TestConversaoMassicaMolar:
    def test_ida_e_volta_e_consistente(self):
        fracoes_massicas = {"agua": 0.6, "etanol": 0.4}
        massas_molares = {"agua": 18.0, "etanol": 46.0}
        molares = fracao_molar_a_partir_massica(fracoes_massicas, massas_molares)
        assert sum(molares.values()) == pytest.approx(1.0)

        massicas_recuperadas = fracao_massica_a_partir_molar(molares, massas_molares)
        assert massicas_recuperadas["agua"] == pytest.approx(fracoes_massicas["agua"], rel=1e-9)
        assert massicas_recuperadas["etanol"] == pytest.approx(fracoes_massicas["etanol"], rel=1e-9)

    def test_componente_mais_leve_tem_fracao_molar_maior_que_massica(self):
        # agua (M=18) e etanol (M=46) 50/50 em massa -> agua deve dominar em base molar
        molares = fracao_molar_a_partir_massica({"agua": 0.5, "etanol": 0.5}, {"agua": 18.0, "etanol": 46.0})
        assert molares["agua"] > 0.5


class TestPressaoParcial:
    def test_lei_de_dalton(self):
        assert pressao_parcial(fracao_molar=0.21, pressao_total=101325.0) == pytest.approx(21278.25)

    def test_componente_puro_igual_pressao_total(self):
        assert pressao_parcial(fracao_molar=1.0, pressao_total=200000.0) == pytest.approx(200000.0)
