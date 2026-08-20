"""Cinética química e dimensionamento de reatores ideais (batelada, CSTR, PFR) para leis de
velocidade de ordem simples — as equações de projeto clássicas de Levenspiel (*Chemical
Reaction Engineering*), aqui restritas às ordens 0, 1 e 2, que têm solução analítica fechada;
ordens fracionárias ou leis de velocidade mais complexas (Langmuir-Hinshelwood, autocatálise)
exigem integração numérica da equação de projeto, fora do escopo de fórmulas fechadas deste
módulo.
"""

import math


def constante_velocidade_arrhenius(A: float, Ea: float, T: float, R: float = 8.314) -> float:
    """Constante de velocidade pela equação de Arrhenius: k = A·exp(-Ea/RT). `Ea` em J/mol
    (mesma base molar de R); T em K."""
    return A * math.exp(-Ea / (R * T))


def taxa_reacao_ordem_n(k: float, C: float, ordem: float) -> float:
    """Lei de velocidade de ordem n: -rA = k·Cⁿ."""
    return k * C ** ordem


def _validar_ordem_suportada(ordem: int) -> None:
    if ordem not in (0, 1, 2):
        raise NotImplementedError(
            f"Solução analítica implementada só para ordem 0, 1 ou 2 (recebeu {ordem}); "
            "outras ordens exigem integração numérica da equação de projeto.")


def tempo_batelada(k: float, CA0: float, CA: float, ordem: int) -> float:
    """Tempo de reação em um reator batelada de volume constante para levar a concentração de
    CA0 a CA, para as ordens com solução analítica fechada:

    - ordem 0: t = (CA0 - CA)/k
    - ordem 1: t = (1/k)·ln(CA0/CA)
    - ordem 2: t = (1/k)·(1/CA - 1/CA0)
    """
    _validar_ordem_suportada(ordem)
    if ordem == 0:
        return (CA0 - CA) / k
    if ordem == 1:
        return (1.0 / k) * math.log(CA0 / CA)
    return (1.0 / k) * (1.0 / CA - 1.0 / CA0)


def tempo_espacial_cstr(k: float, CA0: float, X: float, ordem: int) -> float:
    """Tempo espacial (τ = V/Q) de um CSTR (reator de mistura completa) em regime permanente,
    para atingir a conversão X na saída, avaliando a taxa de reação nas condições de saída
    (definição do CSTR): τ = CA0·X / (-rA)|saída, com -rA = k·(CA0·(1-X))ⁿ."""
    _validar_ordem_suportada(ordem)
    CA_saida = CA0 * (1.0 - X)
    return CA0 * X / taxa_reacao_ordem_n(k, CA_saida, ordem)


def tempo_espacial_pfr(k: float, CA0: float, X: float, ordem: int) -> float:
    """Tempo espacial (τ = V/Q) de um PFR (reator tubular, escoamento empistonado) em regime
    permanente para atingir a conversão X na saída — integral da equação de projeto ao longo do
    reator, com solução analítica para as ordens suportadas:

    - ordem 0: τ = CA0·X/k
    - ordem 1: τ = (1/k)·ln(1/(1-X))
    - ordem 2: τ = X / (k·CA0·(1-X))
    """
    _validar_ordem_suportada(ordem)
    if ordem == 0:
        return CA0 * X / k
    if ordem == 1:
        return (1.0 / k) * math.log(1.0 / (1.0 - X))
    return X / (k * CA0 * (1.0 - X))


def conversao_cstr_primeira_ordem(k: float, tau: float) -> float:
    """Inversa de `tempo_espacial_cstr` para ordem 1: conversão de saída de um CSTR dado o
    tempo espacial, X = k·τ/(1 + k·τ)."""
    return k * tau / (1.0 + k * tau)


def conversao_pfr_primeira_ordem(k: float, tau: float) -> float:
    """Inversa de `tempo_espacial_pfr` para ordem 1: conversão de saída de um PFR dado o tempo
    espacial, X = 1 - exp(-k·τ)."""
    return 1.0 - math.exp(-k * tau)


def numero_damkohler(k: float, tau: float, CA0: float, ordem: float) -> float:
    """Número de Damköhler: razão entre a taxa de reação e a taxa de convecção (Da = k·τ·CA0ⁿ⁻¹),
    o grupo adimensional que determina a conversão atingível em um reator contínuo — Da << 1
    indica conversão baixa (reação lenta frente ao tempo de residência), Da >> 1 indica
    conversão próxima de completa."""
    return k * tau * CA0 ** (ordem - 1.0)
