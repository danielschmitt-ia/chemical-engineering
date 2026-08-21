"""Análise de variabilidade: desvio padrão amostral e coeficiente de variação — a base
estatística sobre a qual o controle estatístico de processo (`controle_estatistico_processo.py`)
constrói seus limites de controle e índices de capacidade."""

import math
from collections.abc import Sequence


def desvio_padrao_amostral(valores: Sequence[float]) -> float:
    """Desvio padrão amostral: s = √[Σ(x_i - x̄)²/(n-1)] — usa n-1 no denominador (correção de
    Bessel), o padrão para dados de processo, onde a amostra observada é tipicamente um
    subconjunto do processo real, não a população inteira."""
    n = len(valores)
    media = sum(valores) / n
    variancia = sum((x - media) ** 2 for x in valores) / (n - 1)
    return math.sqrt(variancia)


def coeficiente_variacao(desvio_padrao: float, media: float) -> float:
    """Coeficiente de variação (CV): desvio padrão relativo à média — CV = s/x̄. Útil para
    comparar a variabilidade de grandezas com médias muito diferentes (ex.: comparar a
    variabilidade de uma vazão de 10 L/min com uma de 10000 L/min, onde o desvio padrão absoluto
    sozinho não é comparável). Retorna uma fração (0-1); multiplique por 100 para porcentagem."""
    return desvio_padrao / media
