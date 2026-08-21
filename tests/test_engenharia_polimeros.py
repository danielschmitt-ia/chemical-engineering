import pytest

from calculos_processo.engenharia_polimeros import (
    grau_polimerizacao,
    indice_polidispersao,
    massa_molar_massa_media,
    massa_molar_numero_medio,
)


class TestMassasMolaresMedias:
    def test_populacao_monodispersa_mn_igual_mw(self):
        Mn = massa_molar_numero_medio([100], [20000.0])
        Mw = massa_molar_massa_media([100], [20000.0])
        assert Mn == pytest.approx(20000.0)
        assert Mw == pytest.approx(20000.0)

    def test_mw_sempre_maior_ou_igual_a_mn(self):
        populacoes = [100, 50, 10]
        massas = [10000.0, 20000.0, 50000.0]
        Mn = massa_molar_numero_medio(populacoes, massas)
        Mw = massa_molar_massa_media(populacoes, massas)
        assert Mw >= Mn


class TestPDI:
    def test_monodispersa_pdi_um(self):
        assert indice_polidispersao(Mw=20000.0, Mn=20000.0) == pytest.approx(1.0)

    def test_polidispersa_pdi_maior_que_um(self):
        assert indice_polidispersao(Mw=22000.0, Mn=15625.0) > 1.0


class TestGrauPolimerizacao:
    def test_formula_direta(self):
        assert grau_polimerizacao(Mn=15625.0, massa_molar_mero=100.0) == pytest.approx(156.25)
