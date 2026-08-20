"""Geração de vapor e cogeração: eficiência de caldeira pelo método direto e as métricas centrais
de desempenho de um sistema de cogeração (heat rate e eficiência global) — a comparação que
justifica cogeração é sempre entre o combustível economizado gerando calor e eletricidade juntos
versus gerando cada um separadamente.
"""


def eficiencia_caldeira(vazao_vapor: float, entalpia_vapor: float, entalpia_agua_alimentacao: float,
                         vazao_combustivel: float, pci_combustivel: float) -> float:
    """Eficiência de caldeira pelo método direto (ASME PTC 4): razão entre a energia útil
    entregue ao vapor e a energia do combustível consumido —

        η = [vazão_vapor·(h_vapor - h_água_alimentação)] / (vazão_combustível·PCI)

    `pci_combustivel`: poder calorífico inferior do combustível (mesma base de massa/volume da
    `vazao_combustivel`). O método direto não decompõe as perdas individuais (gases de exaustão,
    radiação, purga) — para isso, ver o método indireto (perdas), fora do escopo desta função."""
    return (vazao_vapor * (entalpia_vapor - entalpia_agua_alimentacao)) / (vazao_combustivel * pci_combustivel)


def heat_rate_cogeracao(energia_combustivel: float, potencia_eletrica: float) -> float:
    """Heat rate de um sistema de geração de potência: energia de combustível consumida por
    unidade de eletricidade gerada — heat_rate = energia_combustível/potência_elétrica. Quanto
    menor, mais eficiente a conversão de combustível em eletricidade (ignorando o calor útil
    recuperado — ver `eficiencia_global_cogeracao` para a métrica que o inclui)."""
    return energia_combustivel / potencia_eletrica


def eficiencia_global_cogeracao(potencia_eletrica: float, calor_util: float, energia_combustivel: float) -> float:
    """Eficiência global de um sistema de cogeração: (eletricidade gerada + calor útil
    recuperado) / energia de combustível consumida. É a métrica que justifica cogeração — um
    ciclo puramente elétrico tipicamente converte 30-45% do combustível em eletricidade e rejeita
    o resto como calor de baixa qualidade; a cogeração recupera parte desse calor rejeitado como
    vapor/água quente de processo, elevando a eficiência global tipicamente para 65-85%, mesmo
    com a eficiência elétrica isolada ligeiramente menor que um ciclo dedicado."""
    return (potencia_eletrica + calor_util) / energia_combustivel
