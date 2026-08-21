"""Peneiramento e classificação granulométrica: eficiência de peneiramento por balanço de massa
— a fração do material fino da alimentação que efetivamente é recuperada no passante (undersize),
a métrica central de desempenho de uma peneira industrial."""


def eficiencia_peneiramento(massa_passante: float, fracao_fino_passante: float,
                             massa_alimentacao: float, fracao_fino_alimentacao: float) -> float:
    """Eficiência de peneiramento: fração do material fino presente na alimentação que é
    recuperada no passante (undersize) —

        E = (massa_passante·fração_fino_passante) / (massa_alimentação·fração_fino_alimentação)

    Uma peneira ideal (100% de eficiência) recupera todo o fino da alimentação no passante, sem
    nenhum fino "escapando" no retido (oversize). Na prática, E < 1 sempre — parte do fino fica
    presa na camada de material sobre a tela (efeito conhecido como "blinding" ou cegamento) e
    sai pelo retido junto com o material grosso."""
    return (massa_passante * fracao_fino_passante) / (massa_alimentacao * fracao_fino_alimentacao)
