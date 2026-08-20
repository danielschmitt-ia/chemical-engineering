"""Transferência de calor em processos: calor sensível, coeficiente global de troca térmica
(modelo de parede plana, resistências em série) e dimensionamento de trocadores de calor pelo
método da diferença de temperatura média logarítmica (DTML/LMTD).
"""

import math


def calor_sensivel(vazao_massica: float, cp: float, delta_T: float) -> float:
    """Taxa de calor sensível trocada por uma corrente: Q = ṁ·cp·ΔT [W, se ṁ em kg/s e cp em
    J/(kg·K)]. `delta_T` é a variação de temperatura da corrente (T_saída - T_entrada); o sinal
    do resultado indica se a corrente recebe (positivo) ou cede (negativo) calor."""
    return vazao_massica * cp * delta_T


def coeficiente_global_troca(h_quente: float, h_frio: float, espessura_parede: float = 0.0,
                              k_parede: float | None = None, resistencia_incrustacao_quente: float = 0.0,
                              resistencia_incrustacao_fria: float = 0.0) -> float:
    """Coeficiente global de troca térmica U, por unidade de área, modelando a parede do
    trocador como plana (resistências térmicas em série) — simplificação usual para uma
    estimativa de engenharia; para tubos de parede espessa frente ao diâmetro, a curvatura
    introduz um fator de correção adicional que este modelo não captura.

        1/U = 1/h_quente + Rf_quente + espessura_parede/k_parede + Rf_fria + 1/h_frio

    h_quente, h_frio: coeficientes convectivos de película [W/(m²·K)]; espessura_parede [m] e
    k_parede [W/(m·K)] descrevem a condução pela parede (omitidos por padrão: parede ideal, sem
    resistência condutiva); resistencia_incrustacao_* [m²·K/W] são opcionais (fouling), 0 por
    padrão (superfície limpa)."""
    resistencia_total = 1.0 / h_quente + 1.0 / h_frio + resistencia_incrustacao_quente + resistencia_incrustacao_fria
    if espessura_parede > 0:
        if k_parede is None or k_parede <= 0:
            raise ValueError("k_parede precisa ser positivo quando espessura_parede > 0")
        resistencia_total += espessura_parede / k_parede
    return 1.0 / resistencia_total


def diferenca_temperatura_media_log(delta_T1: float, delta_T2: float) -> float:
    """Diferença de temperatura média logarítmica (DTML) entre as duas extremidades de um
    trocador de calor: ΔTml = (ΔT1 - ΔT2)/ln(ΔT1/ΔT2). Quando ΔT1 ≈ ΔT2 (perfil de temperatura
    aproximadamente linear), a fórmula tem uma indeterminação 0/0 removível cujo limite é o
    próprio ΔT1 — usado diretamente nesse caso para evitar divisão por zero numérica."""
    if delta_T1 <= 0 or delta_T2 <= 0:
        raise ValueError("As diferenças de temperatura terminais devem ser positivas "
                          "(sem cruzamento de temperatura entre as correntes)")
    if math.isclose(delta_T1, delta_T2, rel_tol=1e-9):
        return delta_T1
    return (delta_T1 - delta_T2) / math.log(delta_T1 / delta_T2)


def dtml_trocador(T_quente_entrada: float, T_quente_saida: float, T_frio_entrada: float,
                   T_frio_saida: float, arranjo: str = "contracorrente") -> float:
    """DTML de um trocador de calor de dois passes a partir das quatro temperaturas terminais,
    já montando as diferenças ΔT1/ΔT2 corretas conforme o arranjo de escoamento:

    - "contracorrente": ΔT1 = T_quente_entrada - T_frio_saida, ΔT2 = T_quente_saida - T_frio_entrada
    - "cocorrente" (paralelo): ΔT1 = T_quente_entrada - T_frio_entrada, ΔT2 = T_quente_saida - T_frio_saida
    """
    if arranjo == "contracorrente":
        delta_T1 = T_quente_entrada - T_frio_saida
        delta_T2 = T_quente_saida - T_frio_entrada
    elif arranjo == "cocorrente":
        delta_T1 = T_quente_entrada - T_frio_entrada
        delta_T2 = T_quente_saida - T_frio_saida
    else:
        raise ValueError(f"arranjo deve ser 'contracorrente' ou 'cocorrente', recebeu {arranjo!r}")
    return diferenca_temperatura_media_log(delta_T1, delta_T2)


def taxa_calor_trocador(U: float, area: float, dtml: float) -> float:
    """Taxa de calor trocada: Q = U·A·ΔTml [W, se U em W/(m²·K) e A em m²]."""
    return U * area * dtml


def area_troca_termica(Q: float, U: float, dtml: float) -> float:
    """Área de troca térmica necessária para trocar a taxa de calor Q: A = Q/(U·ΔTml) [m²]."""
    return Q / (U * dtml)
