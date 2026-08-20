import pytest

from calculos_processo.lixiviacao import concentracao_lixiviado, rendimento_lixiviacao_estagio_ideal


class TestConcentracaoLixiviado:
    def test_formula_direta(self):
        assert concentracao_lixiviado(50.0, 1000.0) == pytest.approx(0.05)


class TestRendimentoEstagioIdeal:
    def test_formula_direta(self):
        assert rendimento_lixiviacao_estagio_ideal(1000.0, 100.0) == pytest.approx(0.9)

    def test_mais_retencao_reduz_rendimento(self):
        Y_pouca_retencao = rendimento_lixiviacao_estagio_ideal(1000.0, 50.0)
        Y_muita_retencao = rendimento_lixiviacao_estagio_ideal(1000.0, 300.0)
        assert Y_muita_retencao < Y_pouca_retencao

    def test_retencao_maior_que_solvente_e_invalida(self):
        with pytest.raises(ValueError):
            rendimento_lixiviacao_estagio_ideal(100.0, 200.0)
