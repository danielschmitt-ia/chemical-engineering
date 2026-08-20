"""Estudos de confiabilidade (RAM — Reliability, Availability, Maintainability): as métricas
básicas de confiabilidade de um equipamento ou sistema reparável — MTBF, MTTR, disponibilidade e
a confiabilidade (probabilidade de sobreviver sem falha) ao longo do tempo, assumindo o modelo
exponencial de falha (taxa de falha constante — razoável durante a "vida útil" de um equipamento,
depois do período de mortalidade infantil e antes do desgaste, na curva da banheira)."""

import math


def mtbf(tempo_total_operacao: float, numero_falhas: int) -> float:
    """MTBF (Mean Time Between Failures): tempo médio de operação entre falhas sucessivas —
    MTBF = tempo_total_operação / número_de_falhas."""
    return tempo_total_operacao / numero_falhas


def mttr(tempo_total_reparo: float, numero_reparos: int) -> float:
    """MTTR (Mean Time To Repair): tempo médio para restaurar o equipamento após uma falha —
    MTTR = tempo_total_reparo / número_de_reparos."""
    return tempo_total_reparo / numero_reparos


def disponibilidade(mtbf_valor: float, mttr_valor: float) -> float:
    """Disponibilidade em regime permanente de um sistema reparável: A = MTBF/(MTBF+MTTR) — a
    fração do tempo em que o equipamento está operacional. `mtbf_valor` e `mttr_valor` na mesma
    unidade de tempo. Retorna uma fração (0-1); multiplique por 100 para porcentagem."""
    return mtbf_valor / (mtbf_valor + mttr_valor)


def taxa_falha(mtbf_valor: float) -> float:
    """Taxa de falha (λ), o inverso do MTBF, assumindo taxa de falha constante (modelo
    exponencial): λ = 1/MTBF."""
    return 1.0 / mtbf_valor


def confiabilidade_exponencial(t: float, mtbf_valor: float) -> float:
    """Confiabilidade — probabilidade de operar sem falha até o instante t — assumindo o modelo
    exponencial de falha (taxa de falha constante): R(t) = exp(-t/MTBF) = exp(-λt). Só válido
    durante a fase de vida útil da curva da banheira (taxa de falha aproximadamente constante);
    não se aplica durante mortalidade infantil (taxa decrescente) ou desgaste (taxa crescente)."""
    return math.exp(-t / mtbf_valor)
