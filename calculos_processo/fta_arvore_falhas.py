"""Análise de Árvore de Falhas (FTA): a combinação de probabilidades através das duas portas
lógicas básicas de uma árvore de falhas — E (todos os eventos precisam ocorrer) e OU (qualquer
evento é suficiente) — assumindo eventos independentes, a hipótese padrão de uma FTA quantitativa
básica (eventos correlacionados exigem métodos mais avançados, como cut sets com correção de
dependência)."""

from collections.abc import Sequence
from functools import reduce


def probabilidade_porta_e(probabilidades: Sequence[float]) -> float:
    """Probabilidade de saída de uma porta E (AND) — todos os eventos de entrada precisam
    ocorrer simultaneamente: P = P1·P2·...·Pn (eventos independentes). Uma porta E sempre reduz a
    probabilidade (é a lógica por trás da redundância: colocar duas proteções independentes em
    série lógica — ambas precisam falhar para o evento topo ocorrer — reduz drasticamente a
    probabilidade do evento indesejado)."""
    return reduce(lambda a, b: a * b, probabilidades, 1.0)


def probabilidade_porta_ou(probabilidades: Sequence[float]) -> float:
    """Probabilidade de saída de uma porta OU (OR) — qualquer evento de entrada é suficiente:
    P = 1 - (1-P1)·(1-P2)·...·(1-Pn) (eventos independentes) — a probabilidade de que PELO MENOS
    UM dos eventos ocorra é 1 menos a probabilidade de que NENHUM ocorra. Uma porta OU sempre
    aumenta a probabilidade frente a qualquer entrada individual — é a lógica por trás de "mais
    uma coisa pode dar errado, mais provável é a falha"."""
    return 1.0 - reduce(lambda a, b: a * (1.0 - b), probabilidades, 1.0)
