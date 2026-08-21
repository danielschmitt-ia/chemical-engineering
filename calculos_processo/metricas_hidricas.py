"""Métricas de sustentabilidade hídrica: intensidade hídrica e taxa de reúso de água — as duas
métricas centrais para reportar e otimizar o uso de água de um processo industrial."""


def intensidade_hidrica(volume_agua_consumida: float, producao: float) -> float:
    """Intensidade hídrica: volume de água consumida por unidade de produção — a mesma lógica de
    `eficiencia_energetica.consumo_especifico_energia`, aplicada a água em vez de energia
    (ex.: m³ água/t produto)."""
    return volume_agua_consumida / producao


def taxa_reuso_agua(volume_agua_reusada: float, volume_agua_total_utilizada: float) -> float:
    """Taxa de reúso de água: fração do volume total de água utilizada no processo que vem de
    reúso/reciclo interno, em vez de captação nova (água de make-up) — taxa = água_reusada/
    água_total. Retorna uma fração (0-1); água_total = água_reusada + água_de_make-up."""
    return volume_agua_reusada / volume_agua_total_utilizada
