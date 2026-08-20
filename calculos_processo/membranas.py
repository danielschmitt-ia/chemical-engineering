"""Separação por membranas: fluxo de permeado governado pela permeabilidade do material,
seletividade ideal entre dois componentes e coeficiente de rejeição — os três parâmetros básicos
que caracterizam o desempenho de uma membrana (osmose reversa, ultrafiltração, permeação
gasosa).
"""


def fluxo_permeado(permeabilidade: float, espessura: float, forca_motriz: float) -> float:
    """Fluxo de permeado através de uma membrana, modelo de solução-difusão simplificado
    (transporte proporcional à força motriz e inversamente proporcional à espessura, sem
    resistências externas de polarização de concentração): J = (Permeabilidade/espessura)·
    força_motriz. `forca_motriz`: diferença de pressão (permeação gasosa, osmose reversa — nesse
    caso, a diferença de pressão efetiva já descontada da pressão osmótica) ou de concentração
    (diálise), conforme a unidade de `permeabilidade`."""
    return permeabilidade / espessura * forca_motriz


def seletividade_ideal(permeabilidade_A: float, permeabilidade_B: float) -> float:
    """Seletividade ideal de uma membrana entre dois componentes: α = Permeabilidade_A /
    Permeabilidade_B — mesmo papel conceitual da volatilidade relativa em destilação
    (`destilacao.volatilidade_relativa`), mas para separação por membrana. Calculada a partir
    das permeabilidades dos componentes puros; a separação real de uma mistura pode diferir por
    efeitos de acoplamento entre os componentes que permeiam simultaneamente."""
    return permeabilidade_A / permeabilidade_B


def coeficiente_rejeicao(C_permeado: float, C_alimentacao: float) -> float:
    """Coeficiente de rejeição de uma membrana (ex.: osmose reversa, nanofiltração): R = 1 -
    C_permeado/C_alimentação. R=1 (100%) indica rejeição completa do soluto (membrana
    idealmente seletiva pela água); R=0 indica nenhuma rejeição (soluto passa livremente)."""
    return 1.0 - C_permeado / C_alimentacao
