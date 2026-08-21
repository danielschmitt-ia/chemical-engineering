"""Operações de secagem: tempo de secagem no período de taxa constante e no período de taxa
decrescente (assumindo relação linear entre taxa e umidade nesse período — a aproximação usual
quando não se conhece a curva de secagem real do material).

Convenção: X é a umidade livre em base seca (kg água/kg sólido seco, acima da umidade de
equilíbrio); Xc é a umidade crítica onde a taxa de secagem começa a cair.
"""

import math


def tempo_secagem_taxa_constante(Ls: float, A: float, Rc: float, X1: float, Xc: float) -> float:
    """Tempo de secagem no período de taxa constante (evaporação de água livre na superfície,
    taxa limitada pela transferência de calor/massa externa, não pela difusão interna):

        t_c = Ls·(X1 - Xc) / (A·Rc)

    `Ls`: massa de sólido seco [kg]; `A`: área de secagem [m²]; `Rc`: taxa de secagem constante
    [kg água/(m²·h)]; `X1`: umidade livre inicial; `Xc`: umidade livre crítica (onde a taxa
    começa a cair)."""
    return Ls * (X1 - Xc) / (A * Rc)


def tempo_secagem_taxa_decrescente(Ls: float, A: float, Rc: float, Xc: float, X2: float) -> float:
    """Tempo de secagem no período de taxa decrescente, assumindo a aproximação usual de que a
    taxa de secagem cai linearmente com a umidade livre, passando pela origem (R=0 em X=0):

        t_f = (Ls·Xc)/(A·Rc)·ln(Xc/X2)

    `Xc`: umidade livre crítica (início do período); `X2`: umidade livre final desejada. Essa
    aproximação linear é razoável para muitos materiais granulares, mas não vale para sólidos
    onde a difusão interna controla a taxa de forma mais complexa (nesse caso, o período de taxa
    decrescente real precisa de dados experimentais específicos do material)."""
    return (Ls * Xc) / (A * Rc) * math.log(Xc / X2)


def tempo_secagem_total(Ls: float, A: float, Rc: float, X1: float, Xc: float, X2: float) -> float:
    """Tempo total de secagem, soma dos períodos de taxa constante e taxa decrescente. Se
    `X1 <= Xc` (a umidade inicial já está abaixo da crítica), o material entra direto no período
    de taxa decrescente e o termo de taxa constante é zero."""
    t_c = tempo_secagem_taxa_constante(Ls, A, Rc, X1, Xc) if X1 > Xc else 0.0
    return t_c + tempo_secagem_taxa_decrescente(Ls, A, Rc, Xc, X2)
