import pytest

from calculos_processo.transferencia_massa import (
    altura_unidade_transferencia,
    fluxo_convectivo_massa,
    fluxo_difusivo_fick,
    forca_motriz_media_log,
    fracao_nao_recuperada_kremser,
    numero_estagios_kremser,
    numero_unidades_transferencia,
)


class TestFluxos:
    def test_fick_gradiente_negativo_da_fluxo_positivo(self):
        assert fluxo_difusivo_fick(D=1e-9, dC_dx=-100.0) == pytest.approx(1e-7)

    def test_convectivo_proporcional_a_diferenca(self):
        assert fluxo_convectivo_massa(kc=1e-4, C_interface=5.0, C_global=2.0) == pytest.approx(3e-4)


class TestForcaMotrizMediaLog:
    def test_deltas_iguais(self):
        assert forca_motriz_media_log(2.0, 2.0) == pytest.approx(2.0)

    def test_rejeita_nao_positivo(self):
        with pytest.raises(ValueError):
            forca_motriz_media_log(-1.0, 2.0)


class TestNTUHTU:
    def test_altura_coluna_e_htu_vezes_ntu(self):
        HTU = altura_unidade_transferencia(vazao_molar_fase=10.0, coef_global_vezes_area=5.0)
        NTU = numero_unidades_transferencia(y_entrada=0.1, y_saida=0.01, forca_motriz_media=0.03)
        Z = HTU * NTU
        assert HTU == pytest.approx(2.0)
        assert NTU == pytest.approx(3.0)
        assert Z == pytest.approx(6.0)


class TestKremser:
    def test_fator_um_caso_especial(self):
        assert fracao_nao_recuperada_kremser(1.0, N=9) == pytest.approx(0.1)

    def test_mais_estagios_recupera_mais(self):
        phi_poucos = fracao_nao_recuperada_kremser(1.5, N=2)
        phi_muitos = fracao_nao_recuperada_kremser(1.5, N=20)
        assert phi_muitos < phi_poucos

    def test_fator_maior_recupera_mais_para_mesmo_N(self):
        phi_fator_baixo = fracao_nao_recuperada_kremser(1.1, N=5)
        phi_fator_alto = fracao_nao_recuperada_kremser(3.0, N=5)
        assert phi_fator_alto < phi_fator_baixo

    def test_numero_estagios_e_inversa(self):
        phi = fracao_nao_recuperada_kremser(1.4, N=6)
        assert numero_estagios_kremser(1.4, phi) == pytest.approx(6.0)

    def test_numero_estagios_e_inversa_fator_um(self):
        phi = fracao_nao_recuperada_kremser(1.0, N=4)
        assert numero_estagios_kremser(1.0, phi) == pytest.approx(4.0)

    def test_contra_simulacao_estagio_a_estagio(self):
        # Simula a cascata de N estagios diretamente (sistema tridiagonal, com m=1 sem perda de
        # generalidade -- Kremser so depende do fator, nao de L/m/G separadamente) e compara
        # com a formula fechada.
        def simular(A, N, y_Np1=1.0, x0=0.0):
            Mtx = [[0.0] * N for _ in range(N)]
            rhs = [0.0] * N
            for n in range(1, N + 1):
                i = n - 1
                Mtx[i][i] = -(1 + A)
                if n - 1 >= 1:
                    Mtx[i][n - 2] = A
                if n + 1 <= N:
                    Mtx[i][n] = 1.0
                else:
                    rhs[i] -= y_Np1
                if n == 1:
                    rhs[i] -= A * x0
            for col in range(N):
                piv = max(range(col, N), key=lambda r: abs(Mtx[r][col]))
                Mtx[col], Mtx[piv] = Mtx[piv], Mtx[col]
                rhs[col], rhs[piv] = rhs[piv], rhs[col]
                for r in range(col + 1, N):
                    factor = Mtx[r][col] / Mtx[col][col]
                    for c in range(col, N):
                        Mtx[r][c] -= factor * Mtx[col][c]
                    rhs[r] -= factor * rhs[col]
            x = [0.0] * N
            for r in range(N - 1, -1, -1):
                s = rhs[r]
                for c in range(r + 1, N):
                    s -= Mtx[r][c] * x[c]
                x[r] = s / Mtx[r][r]
            return x[0]

        for A in (0.7, 1.4, 2.0):
            for N in (1, 3, 6):
                assert fracao_nao_recuperada_kremser(A, N) == pytest.approx(simular(A, N), abs=1e-9)
