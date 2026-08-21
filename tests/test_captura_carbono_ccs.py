import pytest

from calculos_processo.captura_carbono_ccs import eficiencia_captura, emissao_evitada


class TestEficienciaCaptura:
    def test_formula_direta(self):
        assert eficiencia_captura(massa_co2_capturado=90.0, massa_co2_gerado=100.0) == pytest.approx(0.9)


class TestEmissaoEvitada:
    def test_formula_direta(self):
        assert emissao_evitada(emissao_co2_sem_captura=100.0, emissao_co2_com_captura=15.0) == pytest.approx(85.0)

    def test_evitada_e_menor_que_capturado_por_causa_da_penalidade_energetica(self):
        # 90 capturados, mas so 85 evitados liquidos -- a diferenca e a penalidade energetica
        # da propria unidade de captura (que gera CO2 adicional para operar)
        capturado = 90.0
        evitado = emissao_evitada(100.0, 15.0)
        assert evitado < capturado
