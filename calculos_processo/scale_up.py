"""Scale-up e scale-down de processos: as regras clássicas de escalonamento de agitação
(mantendo similaridade geométrica — mesma razão de aspecto do tanque/impelidor — e escolhendo
qual grandeza de processo manter constante entre as escalas) e uma regra de escalonamento por lei
de potência genérica, aplicável tanto para ampliar um processo de laboratório para planta
(scale-up) quanto para reproduzir em bancada um processo de planta (scale-down, útil para
estudar uma falha ou otimizar condições sem parar a unidade real).

Nenhum critério isolado preserva tudo simultaneamente — aumentar a escala mantendo a potência
por volume constante, por exemplo, MUDA o número de Reynolds e a velocidade de ponta de pá; a
escolha de qual critério manter constante é uma decisão de engenharia baseada em qual fenômeno
domina o processo (mistura controlada por cisalhamento → velocidade de ponta; controlada por
transferência de massa/calor → potência por volume; escoamento laminar → Reynolds).
"""

import math


def velocidade_escala_ponta_pa_constante(N1: float, D1: float, D2: float) -> float:
    """Velocidade de rotação na escala 2 que mantém a velocidade de ponta de pá (πND) constante
    entre as escalas: N2 = N1·(D1/D2). Critério típico quando o cisalhamento na ponta do
    impelidor controla o processo (ex.: sistemas sensíveis a cisalhamento, como cultivo celular)."""
    return N1 * (D1 / D2)


def velocidade_escala_potencia_por_volume_constante(N1: float, D1: float, D2: float) -> float:
    """Velocidade de rotação na escala 2 que mantém a potência por unidade de volume (P/V)
    constante — o critério de scale-up mais comum para processos controlados por transferência
    de massa/calor (já que P/V se correlaciona com o coeficiente de transferência):
    N2 = N1·(D1/D2)^(2/3), derivado de P/V ~ N³D² (com P~N³D⁵ e V~D³) mantido constante."""
    return N1 * (D1 / D2) ** (2.0 / 3.0)


def velocidade_escala_reynolds_constante(N1: float, D1: float, D2: float) -> float:
    """Velocidade de rotação na escala 2 que mantém o número de Reynolds de agitação (ND²)
    constante: N2 = N1·(D1/D2)². Raramente prático em scale-up real (implica velocidades de
    rotação impraticamente baixas em escalas maiores) — mais usado como referência teórica ou
    para regimes puramente laminares."""
    return N1 * (D1 / D2) ** 2


def velocidade_escala_froude_constante(N1: float, D1: float, D2: float) -> float:
    """Velocidade de rotação na escala 2 que mantém o número de Froude de agitação (N²D/g)
    constante: N2 = N1·√(D1/D2). Relevante quando o comportamento do vórtice na superfície
    (tanques sem chicanas) precisa ser preservado entre escalas."""
    return N1 * math.sqrt(D1 / D2)


def escalonamento_lei_potencia(X1: float, S1: float, S2: float, expoente: float) -> float:
    """Regra de escalonamento genérica por lei de potência: X2 = X1·(S2/S1)^expoente. `S1`, `S2`:
    uma medida de escala (ex.: diâmetro do tanque, volume, produção) nas condições 1 e 2; `X1`:
    valor conhecido da grandeza de processo na escala 1 (ex.: tempo de mistura, coeficiente de
    transferência); `expoente`: expoente de escalonamento empírico para essa grandeza específica
    (varia por fenômeno e é tipicamente obtido experimentalmente ou da literatura — ex.: tempo de
    mistura turbulento tipicamente escala com expoente ≈ 2/3 mantendo P/V constante). Cobre tanto
    scale-up (S2 > S1) quanto scale-down (S2 < S1) com a mesma fórmula."""
    return X1 * (S2 / S1) ** expoente
