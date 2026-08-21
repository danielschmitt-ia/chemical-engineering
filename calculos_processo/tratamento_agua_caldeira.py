"""Tratamento de água de caldeira: ciclos de concentração e a vazão de purga (blowdown)
necessária para mantê-los — o controle central para evitar que os sólidos dissolvidos da água de
alimentação se acumulem na caldeira até formar incrustação ou causar arraste (carryover) para o
vapor."""


def ciclos_concentracao(concentracao_purga: float, concentracao_agua_alimentacao: float) -> float:
    """Ciclos de concentração (COC): razão entre a concentração de sólidos dissolvidos (TDS) na
    água de purga e na água de alimentação — COC = TDS_purga/TDS_alimentação. Mesma unidade de
    concentração em ambas (ex.: condutividade ou ppm de TDS, medidas equivalentes na prática).
    Quanto maior o COC operado, menor a purga necessária (economiza água e energia), mas maior o
    risco de incrustação/arraste — o limite prático é definido pelos limites de qualidade de água
    da caldeira (ver a norma/fabricante da caldeira específica)."""
    return concentracao_purga / concentracao_agua_alimentacao


def vazao_purga(vazao_vapor: float, coc: float) -> float:
    """Vazão de purga (blowdown) necessária para manter um ciclo de concentração `coc` alvo, por
    balanço de massa de sólidos na caldeira em regime permanente (o vapor gerado é assumido livre
    de sólidos dissolvidos):

        vazão_purga = vazão_vapor / (COC - 1)

    Requer COC > 1 (senão a purga seria maior que a própria alimentação, fisicamente
    impossível em regime permanente)."""
    if coc <= 1:
        raise ValueError("coc precisa ser maior que 1")
    return vazao_vapor / (coc - 1.0)
