"""Absorção e esgotamento (stripping) em colunas de estágios (pratos): fator de absorção/
esgotamento e número de estágios de equilíbrio pela equação de Kremser
(`transferencia_massa.fracao_nao_recuperada_kremser`), assumindo equilíbrio linear (lei de
Henry, y*=m·x) e a corrente "pobre" entrando livre de soluto (absorvente puro no topo de uma
absorvedora; gás de arraste puro na base de uma esgotadora).
"""

from .transferencia_massa import fracao_nao_recuperada_kremser, numero_estagios_kremser


def fator_absorcao(L: float, m: float, G: float) -> float:
    """Fator de absorção: A = L/(m·G). `L`: vazão molar da fase líquida (absorvente); `G`: vazão
    molar da fase gasosa; `m`: coeficiente de equilíbrio (y*=m·x, lei de Henry). A > 1 favorece
    absorção (a capacidade do líquido de reter soluto, mL, excede a taxa em que o gás o carrega,
    G); quanto maior A, menos estágios são necessários para uma dada recuperação."""
    return L / (m * G)


def fator_esgotamento(G: float, m: float, L: float) -> float:
    """Fator de esgotamento (stripping): S = m·G/L — o inverso do fator de absorção, com os
    papéis de líquido e gás trocados (aqui o gás "arrasta" o soluto para fora do líquido)."""
    return m * G / L


def fracao_nao_absorvida(L: float, m: float, G: float, N: int) -> float:
    """Fração do soluto que permanece não absorvida (sai com o gás de topo) após N estágios de
    equilíbrio, assumindo o absorvente entrando livre de soluto — atalho para
    `fracao_nao_recuperada_kremser(fator_absorcao(L, m, G), N)`."""
    return fracao_nao_recuperada_kremser(fator_absorcao(L, m, G), N)


def fracao_nao_esgotada(G: float, m: float, L: float, N: int) -> float:
    """Fração do soluto que permanece não esgotada (sai com o líquido de fundo) após N estágios
    de equilíbrio, assumindo o gás de arraste entrando livre de soluto — atalho para
    `fracao_nao_recuperada_kremser(fator_esgotamento(G, m, L), N)`."""
    return fracao_nao_recuperada_kremser(fator_esgotamento(G, m, L), N)


def estagios_necessarios_absorcao(L: float, m: float, G: float, fracao_nao_absorvida_alvo: float) -> float:
    """Número de estágios de equilíbrio necessários para atingir uma fração não absorvida alvo
    — atalho para `numero_estagios_kremser(fator_absorcao(L, m, G), fracao_nao_absorvida_alvo)`."""
    return numero_estagios_kremser(fator_absorcao(L, m, G), fracao_nao_absorvida_alvo)
