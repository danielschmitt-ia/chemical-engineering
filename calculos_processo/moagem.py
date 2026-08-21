"""Moagem e redução de tamanho de sólidos: as três leis clássicas de energia de cominuição
(Kick, Rittinger e Bond), cada uma assumindo uma relação diferente entre energia consumida e a
redução de tamanho — Bond é a mais usada na prática industrial por cobrir melhor a faixa de
tamanho intermediária (britagem/moagem grossa) mais comum em plantas de processo.
"""

import math


def energia_lei_kick(Kk: float, F: float, P: float) -> float:
    """Lei de Kick: energia específica de cominuição proporcional ao log da razão de redução:
    E = Kk·ln(F/P). Assume que a energia é proporcional ao volume deformado — mais adequada para
    britagem grossa (redução de tamanho relativamente pequena). `F`, `P`: tamanho característico
    de alimentação e produto (mesma unidade, ex.: diâmetro médio)."""
    return Kk * math.log(F / P)


def energia_lei_rittinger(Kr: float, F: float, P: float) -> float:
    """Lei de Rittinger: energia específica proporcional à área de superfície nova criada:
    E = Kr·(1/P - 1/F). Mais adequada para moagem fina, onde a criação de superfície domina o
    consumo de energia."""
    return Kr * (1.0 / P - 1.0 / F)


def energia_lei_bond(Wi: float, F80: float, P80: float) -> float:
    """Lei de Bond (a mais usada industrialmente, cobre a faixa intermediária entre Kick e
    Rittinger — britagem fina e moagem grossa/média):

        E = 10·Wi·(1/√P80 - 1/√F80)

    `Wi`: índice de trabalho de Bond (work index), específico do material [kWh/t], determinado
    experimentalmente em um moinho de bancada padronizado; `F80`, `P80`: tamanho de abertura de
    peneira que passa 80% da alimentação e do produto, respectivamente, em micrômetros (convenção
    usual — confira as unidades do `Wi` da fonte antes de usar, já que ele foi calibrado para essa
    convenção). Retorna E em kWh/t se `Wi` estiver nessa base."""
    return 10.0 * Wi * (1.0 / math.sqrt(P80) - 1.0 / math.sqrt(F80))
