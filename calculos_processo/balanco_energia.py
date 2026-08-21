"""Balanço de energia em processos: primeira lei da termodinâmica para sistemas abertos em
regime permanente (equação de energia de escoamento em regime permanente — SFEE), aplicável a
qualquer volume de controle com uma entrada e uma saída (trocadores, bombas, turbinas, tubulações
com variação de cota/velocidade). Complementa `balanco_massa.py`: mesma lógica de fechamento de
balanço, agora para energia em vez de massa.
"""

from collections.abc import Sequence


def energia_cinetica_especifica(v: float) -> float:
    """Energia cinética específica (por unidade de massa): ec = v²/2 [J/kg, se v em m/s]."""
    return v ** 2 / 2.0


def energia_potencial_especifica(z: float, g: float = 9.81) -> float:
    """Energia potencial específica (por unidade de massa): ep = g·z [J/kg, se z em m e g em
    m/s²]."""
    return g * z


def balanco_energia_escoamento(delta_h: float, v_entrada: float = 0.0, v_saida: float = 0.0,
                                z_entrada: float = 0.0, z_saida: float = 0.0, g: float = 9.81) -> float:
    """Primeira lei para um volume de controle em regime permanente, uma entrada e uma saída
    (equação de energia de escoamento em regime permanente, SFEE), por unidade de massa:

        q - w_eixo = Δh + Δ(v²/2) + gΔz

    Retorna o lado direito da equação — o calor líquido recebido menos o trabalho de eixo
    fornecido pelo sistema (q - w_eixo) [J/kg] necessário para produzir a variação de entalpia,
    energia cinética e potencial observada entre entrada e saída. `delta_h` é a variação de
    entalpia específica (J/kg); os termos de velocidade e cota default para 0 (aproximação usual
    quando a variação de energia cinética/potencial é desprezível frente à entalpia — válida para
    a maioria dos equipamentos de processo, exceto bocais e turbinas)."""
    delta_ec = energia_cinetica_especifica(v_saida) - energia_cinetica_especifica(v_entrada)
    delta_ep = energia_potencial_especifica(z_saida, g) - energia_potencial_especifica(z_entrada, g)
    return delta_h + delta_ec + delta_ep


def residuo_balanco_energia_global(fluxos_entrada: Sequence[float], fluxos_saida: Sequence[float]) -> float:
    """Resíduo do balanço de energia global em regime permanente (entrada - saída), na mesma
    lógica de `balanco_massa.residuo_balanco_massa_global`: soma de todas as taxas de energia que
    entram no volume de controle (calor, trabalho de eixo, energia carregada pelas correntes de
    massa) menos as que saem [W]. Um resíduo != 0 indica acúmulo de energia (regime transiente)
    ou, na prática, erro de medição/instrumentação."""
    return sum(fluxos_entrada) - sum(fluxos_saida)
