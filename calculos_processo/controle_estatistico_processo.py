"""Controle Estatístico de Processo (CEP/SPC): os limites de controle de Shewhart (3-sigma) para
detectar causas especiais de variação, e os índices de capacidade Cp/Cpk que comparam a
variabilidade natural do processo (`analise_variabilidade.py`) contra os limites de especificação
do produto — a diferença central entre "processo sob controle estatístico" (Shewhart) e "processo
capaz de atender à especificação" (Cp/Cpk): um processo pode estar perfeitamente estável e ainda
assim produzir fora de especificação, se estiver centrado no lugar errado ou for naturalmente
variável demais."""

import math


def limite_controle_superior(media: float, desvio_padrao: float, n_amostra: int = 1) -> float:
    """Limite de controle superior (UCL) de Shewhart, 3-sigma: UCL = x̄ + 3σ/√n. `n_amostra`: o
    tamanho do subgrupo (1 para uma carta de indivíduos; > 1 para uma carta de médias X-barra,
    onde o erro padrão da média diminui com √n)."""
    return media + 3.0 * desvio_padrao / math.sqrt(n_amostra)


def limite_controle_inferior(media: float, desvio_padrao: float, n_amostra: int = 1) -> float:
    """Limite de controle inferior (LCL) de Shewhart, 3-sigma: LCL = x̄ - 3σ/√n."""
    return media - 3.0 * desvio_padrao / math.sqrt(n_amostra)


def indice_capacidade_cp(limite_superior_especificacao: float, limite_inferior_especificacao: float,
                          desvio_padrao: float) -> float:
    """Índice de capacidade potencial Cp: Cp = (USL-LSL)/(6σ) — compara a largura da
    especificação com a variabilidade natural do processo (±3σ), SEM considerar se o processo
    está centrado dentro da especificação. Cp >= 1.33 é um critério comum de "processo capaz"
    (margem de 33% acima do mínimo teórico de Cp=1); Cp alto com Cpk baixo indica um processo
    pouco variável mas mal centrado — ver `indice_capacidade_cpk`."""
    return (limite_superior_especificacao - limite_inferior_especificacao) / (6.0 * desvio_padrao)


def indice_capacidade_cpk(media: float, limite_superior_especificacao: float,
                           limite_inferior_especificacao: float, desvio_padrao: float) -> float:
    """Índice de capacidade real Cpk: Cpk = min[(USL-x̄)/(3σ), (x̄-LSL)/(3σ)] — ao contrário do
    Cp, considera a centralização real do processo, usando a distância até o limite de
    especificação mais próximo. Cpk <= Cp sempre (com igualdade só quando o processo está
    perfeitamente centrado no meio da especificação); Cpk é a métrica que efetivamente prediz a
    fração de produto fora de especificação."""
    cpu = (limite_superior_especificacao - media) / (3.0 * desvio_padrao)
    cpl = (media - limite_inferior_especificacao) / (3.0 * desvio_padrao)
    return min(cpu, cpl)
