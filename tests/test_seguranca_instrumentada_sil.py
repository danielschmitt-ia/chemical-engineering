import pytest

from calculos_processo.seguranca_instrumentada_sil import nivel_sil_a_partir_de_pfd, pfd_media_1oo1


class TestPFDMedia:
    def test_formula_direta(self):
        pfd = pfd_media_1oo1(taxa_falha_perigosa_nao_detectada=1e-6, intervalo_teste_prova=8760.0)
        assert pfd == pytest.approx(1e-6 * 8760.0 / 2.0)

    def test_teste_mais_frequente_reduz_pfd(self):
        pfd_anual = pfd_media_1oo1(1e-6, 8760.0)
        pfd_semestral = pfd_media_1oo1(1e-6, 4380.0)
        assert pfd_semestral < pfd_anual


class TestNivelSIL:
    def test_sil2_na_faixa(self):
        assert nivel_sil_a_partir_de_pfd(0.00438) == 2

    def test_sil1(self):
        assert nivel_sil_a_partir_de_pfd(0.05) == 1

    def test_sil3(self):
        assert nivel_sil_a_partir_de_pfd(5e-4) == 3

    def test_sil4(self):
        assert nivel_sil_a_partir_de_pfd(5e-5) == 4

    def test_fora_da_faixa_levanta_erro(self):
        with pytest.raises(ValueError):
            nivel_sil_a_partir_de_pfd(0.5)
        with pytest.raises(ValueError):
            nivel_sil_a_partir_de_pfd(1e-7)
