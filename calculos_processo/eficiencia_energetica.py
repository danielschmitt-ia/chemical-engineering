"""Eficiência energética: consumo específico de energia (SEC), a métrica padrão para comparar o
desempenho energético de um processo ao longo do tempo ou entre plantas, normalizando pela
produção."""


def consumo_especifico_energia(energia_consumida: float, producao: float) -> float:
    """Consumo específico de energia (Specific Energy Consumption, SEC): energia consumida por
    unidade de produção — SEC = energia_consumida/produção (ex.: GJ/t, kWh/t). Quanto menor, mais
    eficiente energeticamente o processo. A mesma razão, aplicada no nível do site inteiro (em
    vez de uma unidade/produto), é comumente chamada de intensidade energética."""
    return energia_consumida / producao
