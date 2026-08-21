"""Balanço de carbono: emissão de CO2 pela combustão de um combustível, pelo balanço de massa do
carbono (cada átomo de carbono no combustível vira uma molécula de CO2) — o método usado nos
inventários de emissão (ex.: metodologia tier 1 do IPCC) quando a composição exata do
combustível é conhecida em termos de teor de carbono, sem precisar da fórmula estequiométrica
completa de cada componente."""


def emissao_co2_combustao(massa_combustivel: float, fracao_massica_carbono: float) -> float:
    """Massa de CO2 emitida na combustão completa de um combustível, por balanço de massa do
    carbono: cada 12.011 g de carbono (massa molar do C) vira 44.01 g de CO2 (massa molar do
    CO2) —

        massa_CO2 = massa_combustível · fração_mássica_carbono · (44.01/12.011)

    `fracao_massica_carbono`: fração mássica de carbono no combustível (ex.: ~0.75 para diesel,
    ~0.87 para gás natural em base mássica, varia por combustível — obtida da composição/análise
    elementar do combustível específico)."""
    return massa_combustivel * fracao_massica_carbono * (44.01 / 12.011)


def intensidade_carbono(emissao_co2: float, producao: float) -> float:
    """Intensidade de carbono: emissão de CO2 por unidade de produção (ex.: tCO2/t produto,
    kgCO2/kWh gerado) — a métrica usada para comparar a pegada de carbono entre processos ou
    plantas de escalas diferentes, normalizando pela produção."""
    return emissao_co2 / producao
