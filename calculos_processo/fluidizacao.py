"""Fluidização e leitos fluidizados (incluindo leito fluidizado circulante): velocidade mínima
de fluidização pela correlação de Wen & Yu e a queda de pressão do leito já fluidizado —
compartilhado entre reatores de leito fluidizado circulante e operações unitárias de secagem/
mistura de sólidos em leito fluidizado, que usam exatamente os mesmos fundamentos.
"""

import math


def numero_arquimedes(dp: float, rho_particula: float, rho_fluido: float, mu: float, g: float = 9.81) -> float:
    """Número de Arquimedes (Galileu): grupo adimensional que compara a força gravitacional
    líquida (empuxo corrigido) sobre a partícula com as forças viscosas — usado como entrada da
    correlação de Wen & Yu para a velocidade mínima de fluidização:

        Ar = dp³·ρ_fluido·(ρ_partícula - ρ_fluido)·g / μ²
    """
    return dp ** 3 * rho_fluido * (rho_particula - rho_fluido) * g / mu ** 2


def velocidade_minima_fluidizacao(dp: float, rho_particula: float, rho_fluido: float, mu: float,
                                   g: float = 9.81) -> float:
    """Velocidade superficial mínima de fluidização pela correlação de Wen & Yu (1966), a
    correlação clássica de uso mais amplo (não exige conhecer a porosidade no ponto de
    fluidização mínima, ao contrário de resolver a equação de Ergun diretamente):

        Re_mf = sqrt(33.7² + 0.0408·Ar) - 33.7
        v_mf = Re_mf·μ / (ρ_fluido·dp)

    Válida como estimativa de engenharia geral; para um material específico, uma medição direta
    (ou uma correlação ajustada à classificação de Geldart daquele pó) é mais confiável."""
    Ar = numero_arquimedes(dp, rho_particula, rho_fluido, mu, g)
    Re_mf = math.sqrt(33.7 ** 2 + 0.0408 * Ar) - 33.7
    return Re_mf * mu / (rho_fluido * dp)


def queda_pressao_leito_fluidizado(altura_leito: float, epsilon: float, rho_particula: float,
                                    rho_fluido: float, g: float = 9.81) -> float:
    """Queda de pressão de um leito já fluidizado: igual ao peso do leito (partículas +
    fluido intersticial) por unidade de área, corrigido pelo empuxo — praticamente constante
    acima da velocidade mínima de fluidização, ao contrário do leito fixo (onde ΔP cresce com a
    velocidade via Ergun):

        ΔP = (1-ε)·(ρ_partícula - ρ_fluido)·g·altura_leito
    """
    return (1.0 - epsilon) * (rho_particula - rho_fluido) * g * altura_leito
