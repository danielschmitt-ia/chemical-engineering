"""Análise de Modos de Falha e Efeitos (FMEA): o Número de Prioridade de Risco (RPN), a métrica
padrão para priorizar quais modos de falha atacar primeiro, a partir de três avaliações
qualitativas (tipicamente em escala 1-10 cada) feitas pela equipe de FMEA."""


def numero_prioridade_risco(severidade: float, ocorrencia: float, deteccao: float) -> float:
    """Número de Prioridade de Risco (RPN): RPN = Severidade × Ocorrência × Detecção. Cada fator
    tipicamente avaliado em uma escala de 1 (melhor) a 10 (pior) — severidade: gravidade do
    efeito da falha; ocorrência: probabilidade/frequência da causa da falha; detecção: quão
    provável é que os controles atuais detectem a falha antes que o efeito ocorra (10 = falha
    quase certamente não detectada). RPN mais alto indica prioridade maior de ação — mas a
    prática moderna de FMEA (AIAG-VDA) tende a preferir avaliar as três dimensões separadamente
    em vez de um único RPN combinado, já que o produto pode mascarar um fator individual crítico
    (ex.: severidade 9 pode ficar "escondida" atrás de um RPN moderado se ocorrência e detecção
    forem baixas)."""
    return severidade * ocorrencia * deteccao
