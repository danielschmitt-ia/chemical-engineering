"""Engenharia de corrosão: taxa de corrosão a partir da perda de massa de um cupom de teste — o
método padrão (ASTM G1) de quantificar a corrosão de um material em um ambiente específico."""


def taxa_corrosao(perda_massa: float, densidade: float, area_exposta: float, tempo_exposicao: float) -> float:
    """Taxa de corrosão (penetração) a partir da perda de massa de um cupom: a perda de massa
    convertida em perda de espessura (dividindo pela densidade e pela área, o que dá o volume
    perdido por área — uma espessura) e depois pelo tempo de exposição —

        taxa = perda_massa / (densidade · área_exposta · tempo_exposição)

    Retorna a taxa em unidades de comprimento/tempo, consistentes com as unidades de entrada
    (ex.: massa em g, densidade em g/cm³, área em cm², tempo em anos → taxa em cm/ano). Para
    converter para a unidade convencional da indústria (mpy — mils per year), multiplique o
    resultado em cm/ano por 393.7 (1 cm = 10⁴ μm = 10⁴/25.4 mil ≈ 393.7 mil)."""
    return perda_massa / (densidade * area_exposta * tempo_exposicao)
