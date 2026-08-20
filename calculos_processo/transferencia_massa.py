"""Operações unitárias de transferência de massa: lei de Fick, fluxo convectivo, o método de
altura/número de unidades de transferência (HTU/NTU) para contactores contínuos (colunas
recheadas) e a equação de Kremser para cascatas de estágios de equilíbrio em contracorrente — a
base matemática comum compartilhada por absorção/esgotamento (`absorcao_stripping.py`) e
extração líquido-líquido (`extracao_liquido_liquido.py`), que só diferem na definição do fator
(de absorção, esgotamento ou extração).
"""

import math


def fluxo_difusivo_fick(D: float, dC_dx: float) -> float:
    """Fluxo molar difusivo unidimensional pela primeira lei de Fick: J = -D·(dC/dx). `D`:
    difusividade [m²/s]; `dC_dx`: gradiente de concentração [mol/(m³·m)]. O sinal negativo
    reflete que a difusão ocorre no sentido de concentração decrescente; retorna J com esse
    sinal (J > 0 no sentido de x crescente se dC/dx < 0)."""
    return -D * dC_dx


def fluxo_convectivo_massa(kc: float, C_interface: float, C_global: float) -> float:
    """Fluxo convectivo de transferência de massa: N = kc·(C_interface - C_global). `kc`:
    coeficiente convectivo de transferência de massa [m/s]; mesma unidade de concentração em
    ambas as concentrações."""
    return kc * (C_interface - C_global)


def forca_motriz_media_log(delta_C1: float, delta_C2: float) -> float:
    """Força motriz média logarítmica entre dois pontos de um contactor (mesma lógica da DTML de
    `transferencia_calor.diferenca_temperatura_media_log`, aplicada a uma diferença de
    concentração/fração molar em vez de temperatura): ΔC_ml = (ΔC1-ΔC2)/ln(ΔC1/ΔC2), com o limite
    ΔC_ml=ΔC1 quando ΔC1≈ΔC2."""
    if delta_C1 <= 0 or delta_C2 <= 0:
        raise ValueError("As forças motrizes terminais devem ser positivas")
    if math.isclose(delta_C1, delta_C2, rel_tol=1e-9):
        return delta_C1
    return (delta_C1 - delta_C2) / math.log(delta_C1 / delta_C2)


def altura_unidade_transferencia(vazao_molar_fase: float, coef_global_vezes_area: float) -> float:
    """Altura de uma unidade de transferência (HTU) de uma coluna recheada em contato contínuo:
    HTU = G / (Ky·a·S), aqui recebido já como o produto `coef_global_vezes_area` = Ky·a·S
    (coeficiente global de transferência de massa vezes área interfacial específica vezes seção
    transversal) para não impor uma forma específica de estimar Ky·a. Retorna HTU na mesma
    unidade de comprimento implícita em `coef_global_vezes_area`."""
    return vazao_molar_fase / coef_global_vezes_area


def numero_unidades_transferencia(y_entrada: float, y_saida: float, forca_motriz_media: float) -> float:
    """Número de unidades de transferência (NTU): NTU = (y_entrada - y_saida)/ΔC_ml — quantas
    "unidades" de força motriz média a coluna precisa para produzir a variação de composição
    observada. Multiplicado pela HTU (`altura_unidade_transferencia`) dá a altura total de
    recheio necessária: Z = HTU·NTU."""
    return (y_entrada - y_saida) / forca_motriz_media


def fracao_nao_recuperada_kremser(fator: float, N: int) -> float:
    """Equação de Kremser: fração do soluto que permanece não recuperada (não absorvida, não
    esgotada, não extraída — conforme o contexto) após uma cascata de N estágios de equilíbrio
    em contracorrente, com equilíbrio linear (y*=m·x) e a corrente "pobre" entrando livre de
    soluto:

        φ = (K-1)/(K^(N+1) - 1),  K ≠ 1
        φ = 1/(N+1),              K = 1

    `fator` (K) é o fator de absorção (A=L/(mG)), esgotamento (S=mG/L) ou extração (E=m·S/F),
    conforme a aplicação — ver `absorcao_stripping.py` e `extracao_liquido_liquido.py`. Fração
    recuperada = 1 - φ. Verificado por simulação numérica direta da cascata de estágios."""
    if math.isclose(fator, 1.0, rel_tol=1e-9):
        return 1.0 / (N + 1)
    return (fator - 1.0) / (fator ** (N + 1) - 1.0)


def numero_estagios_kremser(fator: float, fracao_nao_recuperada: float) -> float:
    """Inversa de `fracao_nao_recuperada_kremser`: número de estágios de equilíbrio necessários
    para atingir uma fração não recuperada alvo, dado o fator K:

        N = log[(K-1)/φ + 1] / log(K) - 1,  K ≠ 1
        N = 1/φ - 1,                        K = 1
    """
    if math.isclose(fator, 1.0, rel_tol=1e-9):
        return 1.0 / fracao_nao_recuperada - 1.0
    return math.log((fator - 1.0) / fracao_nao_recuperada + 1.0) / math.log(fator) - 1.0
