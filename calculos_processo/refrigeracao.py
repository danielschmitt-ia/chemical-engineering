"""Sistemas de refrigeração industrial: coeficiente de performance (COP) real e o limite teórico
de Carnot — a referência contra a qual qualquer ciclo de refrigeração real é comparado, já que
nenhum ciclo pode superar a eficiência de Carnot operando entre as mesmas duas temperaturas
(segunda lei da termodinâmica)."""


def cop_refrigeracao(Q_evaporador: float, W_compressor: float) -> float:
    """Coeficiente de performance (COP) de refrigeração real: COP = Q_evaporador/W_compressor —
    calor removido no evaporador (o efeito útil de refrigeração) por unidade de trabalho de
    compressão consumido. Mesma unidade de energia/potência em ambos (COP é adimensional)."""
    return Q_evaporador / W_compressor


def cop_carnot_refrigeracao(T_evaporador: float, T_condensador: float) -> float:
    """COP máximo teórico (limite de Carnot) de um ciclo de refrigeração operando entre as
    temperaturas do evaporador e do condensador: COP_Carnot = T_evaporador/(T_condensador -
    T_evaporador). Ambas as temperaturas em Kelvin. Nenhum ciclo real atinge esse limite (a
    segunda lei da termodinâmica o proíbe) — serve como referência de quão distante um ciclo real
    está do ideal, e mostra por que reduzir a diferença de temperatura entre evaporador e
    condensador (ex.: condensador mais bem resfriado) sempre melhora a eficiência possível."""
    return T_evaporador / (T_condensador - T_evaporador)


def cop_carnot_bomba_calor(T_condensador: float, T_evaporador: float) -> float:
    """COP máximo teórico (Carnot) de uma bomba de calor (o mesmo ciclo, mas o efeito útil é o
    calor rejeitado no condensador, não o calor removido no evaporador): COP_Carnot,aquecimento =
    T_condensador/(T_condensador - T_evaporador) = COP_Carnot,refrigeração + 1 — sempre maior que
    o COP de refrigeração entre as mesmas temperaturas, porque o calor rejeitado inclui tanto o
    calor removido do lado frio quanto o próprio trabalho de compressão."""
    return T_condensador / (T_condensador - T_evaporador)
