"""Cristalização e precipitação: supersaturação relativa (a força motriz da nucleação e do
crescimento de cristais), a lei ΔL de McCabe (crescimento de cristal independente do tamanho) e
o rendimento de um cristalizador por balanço de massa com evaporação de solvente.
"""


def supersaturacao_relativa(C: float, C_saturacao: float) -> float:
    """Supersaturação relativa: σ = (C - C_saturação)/C_saturação — a força motriz adimensional
    da nucleação e do crescimento de cristais. σ=0 no equilíbrio (solução saturada, sem força
    motriz); σ>0 indica solução supersaturada (mesma unidade de concentração em C e
    C_saturação)."""
    return (C - C_saturacao) / C_saturacao


def crescimento_cristal_lei_delta_L(taxa_crescimento_linear: float, tempo: float) -> float:
    """Lei ΔL de McCabe: o crescimento linear de um cristal em um dado intervalo de tempo não
    depende do seu tamanho inicial — todos os cristais da população crescem pelo mesmo ΔL,
    preservando a forma da distribuição granulométrica ao longo do tempo (válido quando a taxa
    de crescimento não depende do tamanho, aproximação razoável para muitos sistemas industriais):
    ΔL = G·t. `taxa_crescimento_linear` (G) em comprimento/tempo (ex.: μm/min)."""
    return taxa_crescimento_linear * tempo


def rendimento_cristalizacao(massa_alimentacao: float, fracao_soluto_alimentacao: float,
                              solubilidade_final: float, fracao_solvente_evaporada: float = 0.0) -> float:
    """Rendimento de um cristalizador por balanço de massa em regime permanente, assumindo
    cristais anidros (sem água de hidratação incorporada ao cristal — para sais hidratados o
    balanço precisa contabilizar a água de cristalização à parte) e que o licor-mãe efluente sai
    saturado na condição final:

        cristais = F·x_soluto - solubilidade_final·F·(1-x_soluto)·(1-fração_evaporada)
        rendimento = cristais / (F·x_soluto)

    `solubilidade_final` expressa como massa de soluto por massa de solvente (não por massa de
    solução — confira a convenção da fonte da curva de solubilidade antes de usar).
    `fracao_solvente_evaporada`: fração do solvente da alimentação removida por evaporação antes
    da cristalização (0 se não há evaporação, só resfriamento). Retorna a fração (0-1) do soluto
    alimentado que é recuperada como cristais."""
    soluto_total = massa_alimentacao * fracao_soluto_alimentacao
    solvente_total = massa_alimentacao * (1.0 - fracao_soluto_alimentacao)
    solvente_remanescente = solvente_total * (1.0 - fracao_solvente_evaporada)
    soluto_no_licor_mae = solubilidade_final * solvente_remanescente
    cristais = soluto_total - soluto_no_licor_mae
    return cristais / soluto_total
