import pytest

from calculos_processo.extracao_liquido_liquido import (
    coeficiente_distribuicao,
    estagios_necessarios_extracao,
    fator_extracao,
    fracao_nao_extraida,
    massa_extraida_estagio_unico,
)


class TestCoeficienteDistribuicao:
    def test_definicao_direta(self):
        assert coeficiente_distribuicao(C_extrato=8.0, C_rafinado=2.0) == pytest.approx(4.0)


class TestExtracaoEstagioUnico:
    def test_fator_extracao_um_extrai_metade(self):
        m = massa_extraida_estagio_unico(massa_soluto_alimentacao=100.0, m=2.0, razao_solvente_alimentacao=0.5)
        assert m == pytest.approx(50.0)

    def test_fator_extracao_grande_extrai_quase_tudo(self):
        m = massa_extraida_estagio_unico(massa_soluto_alimentacao=100.0, m=50.0, razao_solvente_alimentacao=10.0)
        assert m == pytest.approx(100.0, rel=1e-2)


class TestCascataCountercorrente:
    def test_fator_extracao(self):
        assert fator_extracao(m=2.0, S=500.0, F=1000.0) == pytest.approx(1.0)

    def test_mais_estagios_extrai_mais(self):
        phi_poucos = fracao_nao_extraida(m=1.5, S=600.0, F=1000.0, N=1)
        phi_muitos = fracao_nao_extraida(m=1.5, S=600.0, F=1000.0, N=8)
        assert phi_muitos < phi_poucos

    def test_estagios_necessarios_recupera_N(self):
        phi = fracao_nao_extraida(m=1.8, S=700.0, F=1000.0, N=4)
        assert estagios_necessarios_extracao(1.8, 700.0, 1000.0, phi) == pytest.approx(4.0)
