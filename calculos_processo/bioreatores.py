"""Bioreatores e engenharia bioquímica: cinética de crescimento microbiano de Monod, crescimento
exponencial em batelada, coeficiente de rendimento biomassa/substrato e taxa de transferência de
oxigênio — os quatro cálculos fundamentais de projeto e operação de um bioreator aeróbio.
"""

import math


def taxa_especifica_crescimento_monod(mu_max: float, S: float, Ks: float) -> float:
    """Taxa específica de crescimento pelo modelo de Monod: μ = μ_max·S/(Ks+S). `S`:
    concentração do substrato limitante; `Ks`: constante de meia saturação (concentração de S na
    qual μ = μ_max/2) — mesma unidade em S e Ks. Para S >> Ks, μ→μ_max (crescimento não limitado
    pelo substrato); para S << Ks, μ cresce aproximadamente linear com S (cinética de
    primeira ordem em S)."""
    return mu_max * S / (Ks + S)


def biomassa_crescimento_exponencial(X0: float, mu: float, t: float) -> float:
    """Concentração de biomassa em crescimento exponencial (batelada, substrato em excesso,
    μ constante): X = X0·exp(μ·t)."""
    return X0 * math.exp(mu * t)


def tempo_duplicacao(mu: float) -> float:
    """Tempo de duplicação da biomassa em crescimento exponencial: td = ln(2)/μ (mesma unidade
    de tempo do inverso de μ)."""
    return math.log(2.0) / mu


def rendimento_biomassa_substrato(biomassa_produzida: float, substrato_consumido: float) -> float:
    """Coeficiente de rendimento biomassa/substrato: Yxs = ΔX/ΔS — massa (ou mols) de biomassa
    produzida por unidade de substrato consumido, ambos como magnitudes positivas na mesma
    unidade de massa/mols."""
    return biomassa_produzida / substrato_consumido


def taxa_transferencia_oxigenio(kLa: float, C_saturacao: float, C_liquido: float) -> float:
    """Taxa volumétrica de transferência de oxigênio da fase gasosa (bolhas) para o caldo de
    fermentação: OTR = kLa·(C* - C_L). `kLa`: coeficiente volumétrico de transferência de massa
    [1/h ou 1/s]; `C_saturacao` (C*): concentração de oxigênio dissolvido em equilíbrio com a
    fase gasosa (solubilidade); `C_liquido` (C_L): concentração real de oxigênio dissolvido no
    caldo. Mesma unidade de concentração em C* e C_L; OTR sai na mesma unidade de concentração
    por unidade de tempo de kLa."""
    return kLa * (C_saturacao - C_liquido)
