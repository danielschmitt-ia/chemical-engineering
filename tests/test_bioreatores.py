import math

import pytest

from calculos_processo.bioreatores import (
    biomassa_crescimento_exponencial,
    rendimento_biomassa_substrato,
    taxa_especifica_crescimento_monod,
    taxa_transferencia_oxigenio,
    tempo_duplicacao,
)


class TestMonod:
    def test_meia_saturacao_da_metade_de_mu_max(self):
        mu = taxa_especifica_crescimento_monod(mu_max=0.8, S=2.0, Ks=2.0)
        assert mu == pytest.approx(0.4)

    def test_substrato_em_excesso_tende_a_mu_max(self):
        mu = taxa_especifica_crescimento_monod(mu_max=0.8, S=1000.0, Ks=2.0)
        assert mu == pytest.approx(0.8, rel=1e-2)


class TestCrescimentoExponencial:
    def test_dobra_apos_um_tempo_de_duplicacao(self):
        mu = 0.3
        td = tempo_duplicacao(mu)
        X = biomassa_crescimento_exponencial(X0=1.0, mu=mu, t=td)
        assert X == pytest.approx(2.0)

    def test_tempo_duplicacao_formula(self):
        assert tempo_duplicacao(mu=0.1) == pytest.approx(math.log(2.0) / 0.1)


class TestRendimentoEOxigenio:
    def test_rendimento_biomassa_substrato(self):
        assert rendimento_biomassa_substrato(biomassa_produzida=5.0, substrato_consumido=10.0) == pytest.approx(0.5)

    def test_otr_positivo_quando_insaturado(self):
        otr = taxa_transferencia_oxigenio(kLa=50.0, C_saturacao=8.0, C_liquido=2.0)
        assert otr == pytest.approx(300.0)

    def test_otr_zero_na_saturacao(self):
        assert taxa_transferencia_oxigenio(kLa=50.0, C_saturacao=8.0, C_liquido=8.0) == pytest.approx(0.0)
