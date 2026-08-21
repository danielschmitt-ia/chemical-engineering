"""Manufatura enxuta na indústria química: OEE (Overall Equipment Effectiveness) — a métrica
central da Manutenção Produtiva Total (TPM) para quantificar as três grandes categorias de perda
de um equipamento (parado, rodando devagar, produzindo com defeito) em um único número."""


def disponibilidade_oee(tempo_operacao: float, tempo_planejado: float) -> float:
    """Componente de disponibilidade do OEE: fração do tempo planejado de produção em que o
    equipamento de fato operou — disponibilidade = tempo_operação/tempo_planejado. Captura perdas
    por paradas (falhas, setup, troca de produto)."""
    return tempo_operacao / tempo_planejado


def performance_oee(contagem_real: float, tempo_ciclo_ideal: float, tempo_operacao: float) -> float:
    """Componente de performance do OEE: fração da velocidade ideal em que o equipamento operou
    enquanto estava rodando — performance = (contagem_real·tempo_ciclo_ideal)/tempo_operação.
    Captura perdas por pequenas paradas e velocidade reduzida frente ao ciclo ideal de projeto."""
    return (contagem_real * tempo_ciclo_ideal) / tempo_operacao


def qualidade_oee(pecas_boas: float, pecas_totais: float) -> float:
    """Componente de qualidade do OEE: fração da produção que sai dentro de especificação, sem
    necessidade de retrabalho — qualidade = peças_boas/peças_totais. Captura perdas por defeito e
    partida (startup, antes do processo estabilizar)."""
    return pecas_boas / pecas_totais


def oee(disponibilidade: float, performance: float, qualidade: float) -> float:
    """OEE (Overall Equipment Effectiveness): o produto dos três componentes —

        OEE = disponibilidade × performance × qualidade

    Um "processo classe mundial" de manufatura discreta é tipicamente citado como OEE >= 85%; a
    indústria de processos contínuos (onde este repositório se insere) costuma usar métricas
    análogas adaptadas (ex.: fator de utilização de planta), já que "peças" e "ciclo ideal" fazem
    menos sentido para um processo contínuo do que para uma linha de manufatura discreta."""
    return disponibilidade * performance * qualidade
