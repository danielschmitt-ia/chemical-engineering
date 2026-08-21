"""Termodinâmica química aplicada a processos: pressão de vapor (Antoine), gás ideal, fator de
compressibilidade, energia livre de Gibbs de reação e sua relação com a constante de equilíbrio,
e a equação de Clausius-Clapeyron para deslocar a pressão de vapor entre temperaturas.
"""

import math


def pressao_vapor_antoine(A: float, B: float, C: float, T: float) -> float:
    """Pressão de vapor pela equação de Antoine: log10(P) = A - B/(C+T).

    As constantes A, B, C e as unidades de P e T (mmHg/°C, bar/K, kPa/°C, ...) dependem
    inteiramente da tabela de onde vieram — não há convenção universal. Use sempre as três
    constantes da mesma fonte/tabela, para o mesmo componente e faixa de temperatura."""
    return 10 ** (A - B / (C + T))


def temperatura_ebulicao_antoine(A: float, B: float, C: float, P: float) -> float:
    """Inversa de `pressao_vapor_antoine`: temperatura na qual a pressão de vapor do componente
    é igual a `P` (ex.: temperatura de ebulição normal, se P for a pressão atmosférica de
    referência da mesma tabela de constantes). T = B/(A - log10(P)) - C."""
    return B / (A - math.log10(P)) - C


def pressao_gas_ideal(n: float, T: float, V: float, R: float = 8.314) -> float:
    """Pressão de um gás ideal: P = nRT/V. Unidades SI por padrão (R em J/(mol·K), V em m³, T em
    K) — retorna P em Pa; use outro R para outro sistema de unidades."""
    return n * R * T / V


def fator_compressibilidade(P: float, V: float, n: float, T: float, R: float = 8.314) -> float:
    """Fator de compressibilidade Z = PV/(nRT), a medida direta do desvio de um gás real em
    relação ao comportamento de gás ideal (Z=1). Mesmas unidades de `pressao_gas_ideal`."""
    return P * V / (n * R * T)


def energia_livre_gibbs_reacao(delta_H: float, T: float, delta_S: float) -> float:
    """Energia livre de Gibbs de reação: ΔG = ΔH - TΔS. Mesma base de quantidade (ex.: J/mol) em
    ΔH e ΔS; T em K. ΔG < 0 indica reação espontânea nas condições dadas."""
    return delta_H - T * delta_S


def constante_equilibrio(delta_G: float, T: float, R: float = 8.314) -> float:
    """Constante de equilíbrio termodinâmica a partir da energia livre de Gibbs de reação:
    K = exp(-ΔG/RT). `delta_G` em J/mol (mesma base molar de R) e T em K."""
    return math.exp(-delta_G / (R * T))


def clausius_clapeyron_pressao(P1: float, T1: float, T2: float, delta_Hvap: float, R: float = 8.314) -> float:
    """Pressão de vapor em uma segunda temperatura pela equação de Clausius-Clapeyron
    (integrada assumindo ΔHvap constante no intervalo e volume molar do líquido desprezível
    frente ao do vapor, tratado como gás ideal):

        ln(P2/P1) = (ΔHvap/R)·(1/T1 - 1/T2)

    P1 é a pressão de vapor conhecida na temperatura T1; retorna P2 na temperatura T2 (mesma
    unidade de P1). `delta_Hvap` em J/mol (mesma base molar de R); T1, T2 em K."""
    return P1 * math.exp((delta_Hvap / R) * (1.0 / T1 - 1.0 / T2))
