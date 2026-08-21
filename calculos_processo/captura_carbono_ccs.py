"""Captura e armazenamento de carbono (CCS): eficiência de captura e emissão evitada — as duas
métricas que definem o desempenho de uma planta de captura, distintas uma da outra porque a
própria captura consome energia (tipicamente gerando emissões adicionais no processo de captura,
compressão e transporte do CO2)."""


def eficiencia_captura(massa_co2_capturado: float, massa_co2_gerado: float) -> float:
    """Eficiência de captura: fração do CO2 gerado pela fonte (ex.: gases de combustão de uma
    planta) que é efetivamente capturada — η = massa_capturada/massa_gerada. Tipicamente 85-95%
    para tecnologias de captura pós-combustão maduras (absorção química com aminas — ver
    `absorcao_stripping.py` para a mesma lógica de estágios de equilíbrio aplicada a essa
    separação); capturar a fração restante fica progressivamente mais caro."""
    return massa_co2_capturado / massa_co2_gerado


def emissao_evitada(emissao_co2_sem_captura: float, emissao_co2_com_captura: float) -> float:
    """Emissão evitada líquida: a redução real de emissão ao adicionar captura, contabilizando a
    penalidade energética do próprio processo de captura (a planta com CCS emite mais CO2 por
    unidade de energia útil gerada do que capturaria "de graça", porque parte da energia da
    planta vai para operar a captura) —

        emissão_evitada = emissão_sem_captura - emissão_com_captura

    `emissao_co2_com_captura` já deve incluir tanto o CO2 residual não capturado quanto qualquer
    emissão adicional da própria unidade de captura (ex.: combustível extra para regenerar o
    solvente de absorção). A emissão evitada é sempre menor que a massa de CO2 capturada — a
    diferença entre as duas é exatamente essa penalidade energética."""
    return emissao_co2_sem_captura - emissao_co2_com_captura
