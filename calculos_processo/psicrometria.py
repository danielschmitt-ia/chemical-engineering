"""Psicrometria e torres de resfriamento: razão de umidade e umidade relativa do ar úmido, e as
duas métricas centrais de desempenho de uma torre de resfriamento (range e approach) — o approach
em particular é o limite termodinâmico fundamental de qualquer torre: a água nunca pode sair mais
fria que a temperatura de bulbo úmido do ar ambiente que a resfria.
"""


def razao_umidade(pressao_vapor_agua: float, pressao_total: float) -> float:
    """Razão de umidade (humidity ratio) do ar úmido: massa de vapor d'água por massa de ar
    seco — W = 0.622·p_w/(P - p_w), com 0.622 ≈ M_água/M_ar_seco (18.015/28.97). `pressao_vapor_
    agua` e `pressao_total` na mesma unidade de pressão."""
    return 0.622 * pressao_vapor_agua / (pressao_total - pressao_vapor_agua)


def umidade_relativa(pressao_vapor_agua: float, pressao_vapor_saturacao: float) -> float:
    """Umidade relativa: UR = p_w/p_sat(T) — a pressão parcial do vapor d'água presente sobre a
    pressão de saturação na mesma temperatura (obtida, por exemplo, da equação de Antoine em
    `termodinamica.pressao_vapor_antoine` para a água). Retorna uma fração (0-1); multiplique por
    100 para porcentagem."""
    return pressao_vapor_agua / pressao_vapor_saturacao


def range_torre_resfriamento(T_agua_quente_entrada: float, T_agua_fria_saida: float) -> float:
    """Range de uma torre de resfriamento: a queda de temperatura da água ao atravessar a torre,
    range = T_entrada(quente) - T_saída(fria) — determinado pela carga térmica que a torre
    precisa rejeitar e pela vazão de água de recirculação (não pelo desempenho da torre em si)."""
    return T_agua_quente_entrada - T_agua_fria_saida


def approach_torre_resfriamento(T_agua_fria_saida: float, T_bulbo_umido_ar: float) -> float:
    """Approach de uma torre de resfriamento: a diferença entre a temperatura da água fria de
    saída e a temperatura de bulbo úmido do ar ambiente — approach = T_saída(fria) -
    T_bulbo_úmido. Ao contrário do range, o approach é a métrica de desempenho da torre em si
    (quão perto do limite termodinâmico ela consegue chegar): um approach menor exige uma torre
    maior/mais eficiente (mais área de enchimento, mais vazão de ar) para a mesma carga térmica —
    a água nunca sai mais fria que a temperatura de bulbo úmido do ar que entra (approach = 0 é o
    limite teórico, inatingível na prática)."""
    return T_agua_fria_saida - T_bulbo_umido_ar
