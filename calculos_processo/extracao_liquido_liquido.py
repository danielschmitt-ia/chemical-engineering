"""Extração líquido-líquido: coeficiente de distribuição, balanço de massa de um único estágio
de equilíbrio e número de estágios em contracorrente pela equação de Kremser
(`transferencia_massa`) — matematicamente idêntica à absorção/esgotamento
(`absorcao_stripping.py`), com o fator de extração no lugar do fator de absorção.
"""

from .transferencia_massa import fracao_nao_recuperada_kremser, numero_estagios_kremser


def coeficiente_distribuicao(C_extrato: float, C_rafinado: float) -> float:
    """Coeficiente de distribuição (partição) do soluto entre as fases, no equilíbrio:
    m = C_extrato/C_rafinado (mesma unidade de concentração em ambas). m > 1 favorece a fase
    extrato (o solvente de extração); é o análogo, em extração líquido-líquido, do coeficiente
    de equilíbrio de absorção/destilação."""
    return C_extrato / C_rafinado


def massa_extraida_estagio_unico(massa_soluto_alimentacao: float, m: float, razao_solvente_alimentacao: float) -> float:
    """Massa de soluto extraída em um único estágio de equilíbrio, contato solvente fresco
    (livre de soluto) com a alimentação: fração extraída = m·(S/F)/(1 + m·(S/F)), onde
    `razao_solvente_alimentacao` é S/F (vazão de solvente sobre vazão de alimentação, mesma
    base de massa/mols). Resultado da mesma unidade de `massa_soluto_alimentacao`."""
    fator = m * razao_solvente_alimentacao
    fracao_extraida = fator / (1.0 + fator)
    return massa_soluto_alimentacao * fracao_extraida


def fator_extracao(m: float, S: float, F: float) -> float:
    """Fator de extração: E = m·S/F. `S`: vazão do solvente de extração; `F`: vazão da
    alimentação (fase a extrair); `m`: coeficiente de distribuição. Mesmo papel matemático do
    fator de absorção em `absorcao_stripping.fator_absorcao` — E > 1 favorece a extração."""
    return m * S / F


def fracao_nao_extraida(m: float, S: float, F: float, N: int) -> float:
    """Fração do soluto que permanece não extraída (sai no rafinado) após N estágios de
    equilíbrio em contracorrente, com solvente fresco entrando livre de soluto — atalho para
    `fracao_nao_recuperada_kremser(fator_extracao(m, S, F), N)`."""
    return fracao_nao_recuperada_kremser(fator_extracao(m, S, F), N)


def estagios_necessarios_extracao(m: float, S: float, F: float, fracao_nao_extraida_alvo: float) -> float:
    """Número de estágios de equilíbrio necessários para atingir uma fração não extraída alvo —
    atalho para `numero_estagios_kremser(fator_extracao(m, S, F), fracao_nao_extraida_alvo)`."""
    return numero_estagios_kremser(fator_extracao(m, S, F), fracao_nao_extraida_alvo)
