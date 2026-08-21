"""Mecânica dos fluidos aplicada a processos: balanço de energia mecânica (Bernoulli estendido,
com trabalho de bomba e perdas), potência de bombeamento e sedimentação de partículas em regime
de Stokes — a base para dimensionar bombas e prever o transporte de sólidos em suspensão.
"""


def trabalho_bomba_necessario(P_entrada: float, P_saida: float, rho: float, v_entrada: float = 0.0,
                               v_saida: float = 0.0, z_entrada: float = 0.0, z_saida: float = 0.0,
                               perdas: float = 0.0, g: float = 9.81) -> float:
    """Balanço de energia mecânica (Bernoulli estendido) entre dois pontos de um sistema de
    bombeamento, por unidade de massa:

        w_bomba = (P_saida - P_entrada)/ρ + Δ(v²/2) + gΔz + perdas

    Retorna o trabalho específico que a bomba precisa fornecer ao fluido [J/kg] para produzir a
    variação de pressão, velocidade e cota observada, mais as perdas por atrito no trajeto
    (`perdas`, também em J/kg — ver `perda_carga.py` para obter ΔP de atrito e dividir por ρ para
    converter para essa base). rho é considerado constante (fluido incompressível)."""
    delta_ec = (v_saida ** 2 - v_entrada ** 2) / 2.0
    delta_ep = g * (z_saida - z_entrada)
    return (P_saida - P_entrada) / rho + delta_ec + delta_ep + perdas


def potencia_hidraulica_bomba(vazao_volumetrica: float, altura_manometrica: float, rho: float,
                               g: float = 9.81) -> float:
    """Potência hidráulica (útil) transferida ao fluido por uma bomba: P = ρ·Q·g·H [W, se Q em
    m³/s, H (altura manométrica total) em m e rho em kg/m³]."""
    return rho * vazao_volumetrica * g * altura_manometrica


def potencia_eixo_bomba(potencia_hidraulica: float, eficiencia: float) -> float:
    """Potência de eixo (potência que o motor precisa fornecer) a partir da potência hidráulica
    e da eficiência global da bomba (0 < eficiencia <= 1): P_eixo = P_hidraulica/eficiencia."""
    if not 0 < eficiencia <= 1:
        raise ValueError("eficiencia deve estar em (0, 1]")
    return potencia_hidraulica / eficiencia


def numero_reynolds_particula(rho_fluido: float, v_relativa: float, d_particula: float, mu_fluido: float) -> float:
    """Número de Reynolds da partícula (mesma definição do Reynolds de tubulação, aplicada ao
    diâmetro da partícula e à velocidade relativa entre partícula e fluido): decide o regime de
    sedimentação — Stokes (Re_p < 1), intermediário ou de Newton (Re_p alto)."""
    return rho_fluido * v_relativa * d_particula / mu_fluido


def velocidade_terminal_stokes(d_particula: float, rho_particula: float, rho_fluido: float, mu_fluido: float,
                                g: float = 9.81) -> float:
    """Velocidade terminal de sedimentação de uma partícula esférica em regime de Stokes
    (arrasto viscoso, sem inércia): v_t = g·d²·(ρ_p - ρ_f) / (18·μ_f).

    Válida apenas para Re_partícula < ~1 (regime laminar de arrasto) — use
    `numero_reynolds_particula` com o `v_t` retornado para conferir a validade; fora dessa faixa,
    o coeficiente de arrasto deixa de ser inversamente proporcional a Re e a fórmula superestima
    a velocidade terminal."""
    return g * d_particula ** 2 * (rho_particula - rho_fluido) / (18.0 * mu_fluido)
