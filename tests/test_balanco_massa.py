import pytest

from calculos_processo.balanco_massa import divisor, misturador, residuo_balanco_massa_global, vazao_desconhecida


class TestVazaoDesconhecida:
    def test_resolve_saida_desconhecida(self):
        assert vazao_desconhecida([100.0, 50.0], [None]) == pytest.approx(150.0)

    def test_resolve_entrada_desconhecida(self):
        assert vazao_desconhecida([100.0, None], [80.0, 90.0]) == pytest.approx(70.0)

    def test_rejeita_mais_de_um_desconhecido(self):
        with pytest.raises(ValueError):
            vazao_desconhecida([100.0, None], [None])

    def test_rejeita_zero_desconhecidos(self):
        with pytest.raises(ValueError):
            vazao_desconhecida([100.0], [100.0])


class TestResiduoBalancoMassaGlobal:
    def test_zero_quando_fecha(self):
        assert residuo_balanco_massa_global([100.0, 50.0], [90.0, 60.0]) == pytest.approx(0.0)

    def test_positivo_quando_falta_saida(self):
        assert residuo_balanco_massa_global([100.0], [80.0]) == pytest.approx(20.0)


class TestMisturador:
    def test_vazao_total_soma_entradas(self):
        vazao, _ = misturador([(100.0, {"A": 1.0}), (50.0, {"A": 1.0})])
        assert vazao == pytest.approx(150.0)

    def test_composicao_media_ponderada(self):
        # 100 kg/h de A puro + 100 kg/h de B puro -> 50/50 em massa
        _, fracoes = misturador([(100.0, {"A": 1.0, "B": 0.0}), (100.0, {"A": 0.0, "B": 1.0})])
        assert fracoes["A"] == pytest.approx(0.5)
        assert fracoes["B"] == pytest.approx(0.5)

    def test_fracoes_da_mistura_somam_um(self):
        _, fracoes = misturador([(30.0, {"A": 0.2, "B": 0.8}), (70.0, {"A": 0.6, "B": 0.4})])
        assert sum(fracoes.values()) == pytest.approx(1.0)

    def test_rejeita_lista_vazia(self):
        with pytest.raises(ValueError):
            misturador([])


class TestDivisor:
    def test_distribui_conforme_fracoes(self):
        saidas = divisor(100.0, {"reciclo": 0.3, "purga": 0.7})
        assert saidas["reciclo"] == pytest.approx(30.0)
        assert saidas["purga"] == pytest.approx(70.0)

    def test_saidas_somam_entrada(self):
        saidas = divisor(200.0, {"a": 0.25, "b": 0.25, "c": 0.5})
        assert sum(saidas.values()) == pytest.approx(200.0)

    def test_rejeita_fracoes_que_nao_somam_um(self):
        with pytest.raises(ValueError):
            divisor(100.0, {"a": 0.5, "b": 0.4})
