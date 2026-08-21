"""Engenharia de partículas: os diâmetros médios de uma distribuição granulométrica — o
aritmético (simples) e o de Sauter (superfície-volume), a definição correta a usar sempre que a
razão área/volume da partícula importa para o fenômeno de interesse (transferência de massa/calor
entre a partícula e o fluido, reação heterogênea — ex.: o módulo de Thiele de
`reatores_leito_fixo.py` é sensível à área superficial específica do catalisador)."""

from collections.abc import Sequence


def diametro_medio_aritmetico(diametros: Sequence[float], quantidades: Sequence[float]) -> float:
    """Diâmetro médio aritmético (D10, base em número): D̄ = Σ(n_i·d_i)/Σn_i — a média simples
    ponderada pela contagem de partículas em cada classe de tamanho."""
    return sum(n * d for n, d in zip(quantidades, diametros)) / sum(quantidades)


def diametro_medio_sauter(diametros: Sequence[float], quantidades: Sequence[float]) -> float:
    """Diâmetro médio de Sauter (D32, superfície-volume): D32 = Σ(n_i·d_i³)/Σ(n_i·d_i²) — o
    diâmetro de uma partícula esférica hipotética com a mesma razão área/volume que a distribuição
    real como um todo. É a definição de diâmetro médio relevante sempre que a área superficial por
    unidade de volume controla o fenômeno (transferência de massa/calor partícula-fluido, cinética
    de reação heterogênea, atomização de sprays) — diferente do diâmetro médio aritmético, que só
    captura o tamanho "típico" sem peso para a área que ele expõe."""
    numerador = sum(n * d ** 3 for n, d in zip(quantidades, diametros))
    denominador = sum(n * d ** 2 for n, d in zip(quantidades, diametros))
    return numerador / denominador
