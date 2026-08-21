"""Tubulações industriais (piping): dimensionamento por velocidade recomendada, espessura
mínima de parede sob pressão interna (fórmula de Barlow, base da norma ASME B31.3) e dilatação
térmica — incluindo a tensão admissível de expansão térmica que baliza uma análise de
flexibilidade de tubulações.

Análise de flexibilidade completa (roteamento, suportação, cargas em bocais de equipamento) exige
software de análise de tensões (ex.: CAESAR II) rodando um modelo de elementos finitos da linha
real — fora do escopo de fórmulas fechadas. O que este módulo fornece é a tensão admissível
(`tensao_admissivel_expansao_termica`) contra a qual a tensão de expansão calculada por esse
software é comparada, e a dilatação livre de um trecho reto, útil para uma estimativa preliminar
de quanto uma linha vai se mover."""

import math


def diametro_a_partir_de_velocidade(vazao_volumetrica: float, velocidade_recomendada: float) -> float:
    """Diâmetro interno necessário para que o escoamento fique próximo de uma velocidade alvo
    (ex.: 1-3 m/s para líquidos, 15-30 m/s para vapor/gás — valores de referência típicos de
    projeto, não uma otimização econômica): D = sqrt(4Q/(π·v))."""
    return math.sqrt(4.0 * vazao_volumetrica / (math.pi * velocidade_recomendada))


def espessura_minima_parede(P: float, D: float, S: float, E: float = 1.0, Y: float = 0.4,
                             sobreespessura: float = 0.0) -> float:
    """Espessura mínima de parede de um tubo reto sob pressão interna, pela fórmula de Barlow
    (base do cálculo de espessura da norma ASME B31.3):

        t = P·D / (2·(S·E + P·Y)) + sobreespessura

    P: pressão de projeto; D: diâmetro externo do tubo; S: tensão admissível do material na
    temperatura de projeto; E: fator de qualidade da junta soldada (1.0 para tubo sem costura);
    Y: coeficiente que depende do material e da temperatura (0.4 é o valor usual para aços
    ferríticos/austeníticos abaixo da temperatura de transição fluência-controlada — ver
    ASME B31.3 Tabela 304.1.1 para outros casos). `sobreespessura` soma uma margem para corrosão
    e tolerância de fabricação, aplicada depois do cálculo estrutural. Mesma unidade de pressão
    em P, S; mesma unidade de comprimento em D, sobreespessura e no resultado."""
    return P * D / (2.0 * (S * E + P * Y)) + sobreespessura


def dilatacao_termica_tubulacao(comprimento: float, coeficiente_dilatacao: float, delta_T: float) -> float:
    """Dilatação térmica linear livre de um trecho reto de tubulação: ΔL = L·α·ΔT. `L` no
    comprimento do trecho, `coeficiente_dilatacao` (α) o coeficiente de dilatação térmica linear
    do material [1/K], `delta_T` a variação de temperatura entre a condição de instalação e a de
    operação [K]. É a dilatação livre (sem restrição) — o que uma análise de flexibilidade
    absorve através de curvas, liras de expansão ou juntas, não a tensão resultante."""
    return comprimento * coeficiente_dilatacao * delta_T


def tensao_admissivel_expansao_termica(Sc: float, Sh: float, f: float = 1.0) -> float:
    """Tensão admissível para a faixa de expansão térmica (ASME B31.3, eq. 1c):

        S_a = f·(1.25·S_c + 0.25·S_h)

    Sc: tensão admissível do material a frio; Sh: tensão admissível do material na temperatura
    de operação (quente); f: fator de redução por número de ciclos térmicos ao longo da vida útil
    (1.0 para até ~7000 ciclos equivalentes a plena amplitude; menor que 1.0 para serviço mais
    cíclico — ver ASME B31.3 para a tabela de f por número de ciclos). O resultado é o limite
    contra o qual se compara a tensão de expansão térmica calculada para o roteamento real da
    linha (via análise de flexibilidade)."""
    return f * (1.25 * Sc + 0.25 * Sh)
