"""Sedimentação e decantação: a correção de sedimentação dificultada (hindered settling) de
Richardson-Zaki, que reduz a velocidade de sedimentação de Stokes (`mecanica_fluidos.
velocidade_terminal_stokes`) quando a fração de sólidos deixa de ser diluída — partículas
vizinhas interferem no escoamento de retorno do fluido deslocado, o efeito central que limita a
capacidade de um decantador/espessador industrial (onde a concentração de sólidos é bem maior do
que a diluição infinita assumida pela lei de Stokes isolada)."""


def velocidade_sedimentacao_dificultada(v_stokes: float, epsilon: float, n: float = 4.65) -> float:
    """Correção de Richardson-Zaki para sedimentação dificultada (hindered settling):

        v = v_Stokes · ε^n

    `epsilon`: porosidade da suspensão (fração volumétrica de líquido, 1 - fração de sólidos);
    `n` ≈ 4.65 é o valor assintótico para regime laminar (Re_partícula < 0.2 — ver
    `mecanica_fluidos.numero_reynolds_particula`); a correlação original de Richardson-Zaki
    (1954) tabula valores menores de n (até ~2.4) para Re_partícula mais alto, então confira o
    regime antes de usar o `n` padrão. Em suspensão diluída (ε→1), v→v_Stokes; conforme a fração
    de sólidos aumenta (ε→0), a sedimentação desacelera fortemente."""
    return v_stokes * epsilon ** n


def fluxo_massico_solidos(concentracao_solidos: float, velocidade_sedimentacao: float) -> float:
    """Fluxo mássico de sólidos em um decantador/espessador: G = C·v — a grandeza central no
    dimensionamento de espessadores contínuos (método de Coe-Clevenger/Kynch): a área mínima do
    espessador é fixada pela concentração em que esse fluxo é mínimo ao longo do perfil de
    concentração do equipamento, não pela concentração de alimentação. `concentracao_solidos`:
    massa de sólidos por volume de suspensão."""
    return concentracao_solidos * velocidade_sedimentacao
