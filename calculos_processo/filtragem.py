"""Filtragem industrial: filtração em torta a pressão constante, pela equação de Ruth —
resistência da torta (proporcional ao volume filtrado) em série com a resistência do meio
filtrante, o modelo clássico usado para escalonar um filtro de laboratório para a planta.
"""


def taxa_filtracao(V: float, alpha: float, Cs: float, Rm: float, mu: float, delta_P: float, A: float) -> float:
    """Taxa instantânea de filtração a pressão constante (equação de Ruth): dV/dt =
    ΔP·A² / [μ·(α·Cs·V + Rm·A)]. `alpha`: resistência específica da torta [m/kg]; `Cs`:
    concentração mássica de sólidos na suspensão [kg/m³]; `Rm`: resistência do meio filtrante
    [1/m]; `mu`: viscosidade do filtrado [Pa·s]; `A`: área de filtração [m²]. A resistência total
    cresce com V (torta se acumula), então a taxa cai ao longo da filtração a ΔP constante."""
    return delta_P * A ** 2 / (mu * (alpha * Cs * V + Rm * A))


def tempo_filtracao_pressao_constante(V: float, alpha: float, Cs: float, Rm: float, mu: float,
                                       delta_P: float, A: float) -> float:
    """Tempo para filtrar um volume V a pressão constante — integral da equação de Ruth desde
    V=0:

        t = (μ·α·Cs)/(2·ΔP·A²)·V² + (μ·Rm)/(ΔP·A)·V

    O primeiro termo (quadrático em V) é a resistência da torta acumulada; o segundo (linear em
    V) é a resistência do meio filtrante. Na prática, α, Cs e Rm são obtidos ajustando esta
    equação (na forma t/V versus V, linear) a dados de um teste de filtração em bancada."""
    return (mu * alpha * Cs) / (2.0 * delta_P * A ** 2) * V ** 2 + (mu * Rm) / (delta_P * A) * V
