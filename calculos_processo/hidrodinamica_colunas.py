"""Hidrodinâmica de colunas (pratos e recheio): parâmetro de fluxo de Fair e a equação de
Souders-Brown para a velocidade de inundação — o limite hidráulico que fixa o diâmetro mínimo de
uma coluna de destilação/absorção. O fator de capacidade C_sb da equação de Souders-Brown vem de
uma correlação gráfica (Fair) específica do tipo de prato/recheio e do espaçamento entre pratos —
não é reproduzido aqui; esta função assume que ele já foi obtido dessa correlação.
"""

import math


def parametro_fluxo_fair(L: float, G: float, rho_vapor: float, rho_liquido: float) -> float:
    """Parâmetro de fluxo (abcissa da correlação de Fair, usada para obter o fator de capacidade
    C_sb em uma correlação gráfica de inundação): F_LV = (L/G)·sqrt(ρ_vapor/ρ_líquido). `L`, `G`:
    vazões mássicas de líquido e vapor (mesma unidade em ambas)."""
    return (L / G) * math.sqrt(rho_vapor / rho_liquido)


def velocidade_inundacao_souders_brown(C_sb: float, rho_liquido: float, rho_vapor: float) -> float:
    """Velocidade superficial de inundação (o limite hidráulico acima do qual o vapor arrasta
    líquido para o prato superior, inundando a coluna) pela equação de Souders-Brown:

        v_inundação = C_sb·sqrt((ρ_líquido - ρ_vapor)/ρ_vapor)

    `C_sb` é o fator de capacidade, obtido de uma correlação gráfica (ex.: Fair) em função do
    parâmetro de fluxo (`parametro_fluxo_fair`) e do espaçamento entre pratos — não calculado
    por esta função. O diâmetro de projeto usual opera a uma fração (tipicamente 70-85%) dessa
    velocidade de inundação, nunca no limite."""
    return C_sb * math.sqrt((rho_liquido - rho_vapor) / rho_vapor)
