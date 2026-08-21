"""Evaporação e concentração de soluções: balanço de massa de um evaporador de efeito único
(o soluto não evapora — sai inteiramente concentrado no líquido) e a economia de vapor, a métrica
central de eficiência energética de um sistema de evaporação."""


def concentracao_final_evaporador(F: float, xF: float, V: float) -> float:
    """Concentração final da solução concentrada, por balanço de massa do soluto (que não
    evapora) em um evaporador de efeito único em regime permanente: F·xF = (F-V)·xL =>
    xL = F·xF/(F-V). `F`: vazão mássica de alimentação; `xF`: fração mássica de soluto na
    alimentação; `V`: vazão mássica de vapor gerado (evaporado)."""
    return F * xF / (F - V)


def vapor_gerado_evaporador(F: float, xF: float, xL: float) -> float:
    """Inversa de `concentracao_final_evaporador`: vazão de vapor que precisa ser evaporada para
    atingir uma concentração final `xL` desejada: V = F·(1 - xF/xL)."""
    return F * (1.0 - xF / xL)


def economia_vapor(V: float, S: float) -> float:
    """Economia de vapor: razão entre o vapor evaporado do produto (V) e o vapor vivo consumido
    no aquecimento (S), a métrica central de eficiência de um evaporador. Economia ≈ 1 para um
    efeito único ideal (sem perdas); sistemas de múltiplo efeito ou com recompressão de vapor
    (TVR/MVR) buscam economia > 1, reaproveitando o calor latente do vapor gerado em efeitos
    subsequentes."""
    return V / S
