"""Eletroquímica industrial e eletrólise: lei de Faraday (relação exata entre carga elétrica e
quantidade de substância eletrolisada) e a equação de Nernst para o potencial de eletrodo fora
das condições padrão.
"""

import math

FARADAY = 96485.0  # C/mol — constante de Faraday


def mols_produzidos_faraday(corrente: float, tempo: float, n_eletrons: float, F: float = FARADAY) -> float:
    """Lei de Faraday da eletrólise: mols de substância produzida/consumida em um eletrodo,
    n = I·t / (n_elétrons·F). `corrente` (I) em A, `tempo` (t) em s, `n_eletrons` o número de
    elétrons trocados por mol da espécie na semirreação (ex.: 2 para Cu²⁺ + 2e⁻ → Cu)."""
    return corrente * tempo / (n_eletrons * F)


def massa_produzida_faraday(corrente: float, tempo: float, massa_molar: float, n_eletrons: float,
                             F: float = FARADAY) -> float:
    """Massa de substância produzida/consumida em um eletrodo: m = I·t·M / (n_elétrons·F).
    `massa_molar` (M) na mesma base de massa desejada no resultado (ex.: g/mol -> resultado em
    g)."""
    return mols_produzidos_faraday(corrente, tempo, n_eletrons, F) * massa_molar


def tempo_necessario_faraday(massa_alvo: float, corrente: float, massa_molar: float, n_eletrons: float,
                              F: float = FARADAY) -> float:
    """Inversa de `massa_produzida_faraday`: tempo necessário para produzir uma massa alvo em
    uma corrente constante, t = massa_alvo·n_elétrons·F / (I·M) [s]."""
    return massa_alvo * n_eletrons * F / (corrente * massa_molar)


def eficiencia_corrente(massa_real: float, massa_teorica: float) -> float:
    """Eficiência de corrente (eficiência faradaica): fração da carga elétrica que efetivamente
    produziu o produto desejado, em vez de se perder em reações paralelas (ex.: evolução de
    hidrogênio competindo com deposição metálica): η = massa_real/massa_teórica, onde
    massa_teórica vem de `massa_produzida_faraday` assumindo 100% de eficiência."""
    return massa_real / massa_teorica


def potencial_nernst(E0: float, T: float, n_eletrons: float, Q: float, R: float = 8.314,
                      F: float = FARADAY) -> float:
    """Potencial de eletrodo fora das condições padrão, pela equação de Nernst:
    E = E0 - (RT)/(n_elétrons·F)·ln(Q). `E0`: potencial padrão do par redox [V]; `Q`: quociente
    de reação (razão das atividades/concentrações dos produtos sobre reagentes, cada uma elevada
    ao seu coeficiente estequiométrico); T em K."""
    return E0 - (R * T) / (n_eletrons * F) * math.log(Q)
