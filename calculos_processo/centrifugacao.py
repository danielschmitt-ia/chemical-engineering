"""Centrifugação industrial: a aceleração centrífuga expressa como múltiplo da gravidade (a
métrica padrão de especificação de uma centrífuga) e a velocidade terminal de sedimentação sob
campo centrífugo — a mesma lei de Stokes de `mecanica_fluidos.velocidade_terminal_stokes`, com a
aceleração centrífuga ω²r no lugar de g, a base do dimensionamento de centrífugas de decantação.
"""


def forca_g_centrifuga(omega: float, r: float, g: float = 9.81) -> float:
    """Aceleração centrífuga como múltiplo da gravidade (o "número de g" usado para especificar
    uma centrífuga): (ω²r)/g. `omega`: velocidade angular [rad/s]; `r`: raio (posição radial,
    tipicamente o raio do tambor/bowl) [m]."""
    return omega ** 2 * r / g


def velocidade_sedimentacao_centrifuga(d_particula: float, rho_particula: float, rho_fluido: float,
                                        mu_fluido: float, omega: float, r: float) -> float:
    """Velocidade terminal de sedimentação sob campo centrífugo, regime de Stokes — a lei de
    Stokes com a aceleração centrífuga ω²r substituindo g:

        v = ω²r·d²·(ρ_p - ρ_f) / (18·μ_f)

    Válida na mesma faixa de Reynolds de partícula que a sedimentação gravitacional (Re_p < ~1);
    como ω²r tipicamente excede g em várias ordens de grandeza, é isso que torna a centrifugação
    capaz de separar partículas pequenas demais para sedimentar por gravidade em tempo prático."""
    return omega ** 2 * r * d_particula ** 2 * (rho_particula - rho_fluido) / (18.0 * mu_fluido)
