"""Mistura e agitação de fluidos: os grupos adimensionais e a correlação de potência usados para
especificar um agitador — número de Reynolds de agitação (regime de escoamento no tanque),
número de Froude (relevante para a formação de vórtice em tanques sem chicanas) e a potência
consumida pelo impelidor a partir do número de potência (obtido experimentalmente por tipo de
impelidor, ex.: turbina Rushton, hélice marinha)."""


def numero_reynolds_agitacao(rho: float, N: float, D: float, mu: float) -> float:
    """Número de Reynolds de agitação: Re = ρ·N·D²/μ. `N`: velocidade de rotação [rev/s]; `D`:
    diâmetro do impelidor [m]. Re < ~10 indica regime laminar, Re > ~10<sup>4</sup> regime
    turbulento plenamente desenvolvido (a faixa de transição depende do tipo de impelidor)."""
    return rho * N * D ** 2 / mu


def numero_froude_agitacao(N: float, D: float, g: float = 9.81) -> float:
    """Número de Froude de agitação: Fr = N²D/g — relação entre forças inerciais e
    gravitacionais, relevante para prever a profundidade do vórtice em tanques sem chicanas
    (baffles); com chicanas, o vórtice é suprimido e Fr deixa de ser relevante para a potência."""
    return N ** 2 * D / g


def potencia_agitador(Po: float, rho: float, N: float, D: float) -> float:
    """Potência consumida pelo impelidor, a partir do número de potência: P = Po·ρ·N³·D⁵ [W, se
    ρ em kg/m³, N em rev/s, D em m]. `Po` (número de potência) é obtido experimentalmente para
    cada tipo de impelidor, tipicamente como uma correlação Po(Re) específica (constante no
    regime turbulento para a maioria dos impelidores) — não calculado por esta função."""
    return Po * rho * N ** 3 * D ** 5
