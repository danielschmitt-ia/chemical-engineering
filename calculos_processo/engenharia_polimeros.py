"""Engenharia de polímeros: as massas molares médias que caracterizam uma distribuição de
tamanho de cadeia polimérica (Mn, Mw), o índice de polidispersão que resume a largura dessa
distribuição, e o grau de polimerização médio."""

from collections.abc import Sequence


def massa_molar_numero_medio(populacoes: Sequence[float], massas_molares: Sequence[float]) -> float:
    """Massa molar número-média: Mn = Σ(N_i·M_i)/ΣN_i — a média simples ponderada pelo número de
    cadeias em cada classe de massa molar. Sensível ao número de cadeias pequenas (cada cadeia
    conta igualmente, independente do seu tamanho)."""
    return sum(n * m for n, m in zip(populacoes, massas_molares)) / sum(populacoes)


def massa_molar_massa_media(populacoes: Sequence[float], massas_molares: Sequence[float]) -> float:
    """Massa molar massa-média: Mw = Σ(N_i·M_i²)/Σ(N_i·M_i) — ponderada pela massa (não pelo
    número) de cada classe, então mais sensível à presença de cadeias grandes que Mn. Sempre
    Mw >= Mn (com igualdade só para uma distribuição perfeitamente monodispersa — todas as cadeias
    do mesmo tamanho)."""
    numerador = sum(n * m ** 2 for n, m in zip(populacoes, massas_molares))
    denominador = sum(n * m for n, m in zip(populacoes, massas_molares))
    return numerador / denominador


def indice_polidispersao(Mw: float, Mn: float) -> float:
    """Índice de polidispersão (PDI, ou Đ na notação IUPAC): PDI = Mw/Mn — a largura relativa da
    distribuição de massa molar. PDI=1 é uma distribuição perfeitamente monodispersa (só possível
    na prática para biopolímeros ou polímeros sintetizados por técnicas de polimerização viva);
    polímeros comerciais típicos têm PDI entre 2 e 20+, dependendo do mecanismo de polimerização."""
    return Mw / Mn


def grau_polimerizacao(Mn: float, massa_molar_mero: float) -> float:
    """Grau de polimerização médio (número de unidades repetitivas por cadeia, em média):
    DP = Mn/M0, onde M0 é a massa molar do mero (a unidade repetitiva do polímero)."""
    return Mn / massa_molar_mero
