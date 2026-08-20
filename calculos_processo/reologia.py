"""Reologia de fluidos não-newtonianos: modelos de lei de potência (Ostwald-de Waele) e
plástico de Bingham, e o número de Reynolds generalizado de Metzner-Reed para escoamento de
fluidos de lei de potência em tubulações — necessário porque a definição usual de Reynolds
(`perda_carga.numero_reynolds`) assume viscosidade newtoniana constante, que não existe aqui.
"""


def tensao_cisalhante_lei_potencia(K: float, taxa_deformacao: float, n: float) -> float:
    """Modelo de lei de potência (Ostwald-de Waele): τ = K·γ̇ⁿ. `K` é o índice de consistência
    [Pa·sⁿ], `taxa_deformacao` (γ̇) a taxa de cisalhamento [1/s] e `n` o índice de
    comportamento (n=1 recupera um fluido newtoniano de viscosidade K; n<1 pseudoplástico,
    "shear-thinning"; n>1 dilatante, "shear-thickening")."""
    return K * taxa_deformacao ** n


def viscosidade_aparente_lei_potencia(K: float, taxa_deformacao: float, n: float) -> float:
    """Viscosidade aparente de um fluido de lei de potência na taxa de cisalhamento dada:
    μ_ap = τ/γ̇ = K·γ̇ⁿ⁻¹ — diferente de um fluido newtoniano, varia com a própria taxa de
    cisalhamento, então só tem sentido físico associada a um γ̇ específico."""
    return K * taxa_deformacao ** (n - 1.0)


def tensao_cisalhante_bingham(tau0: float, mu_plastico: float, taxa_deformacao: float) -> float:
    """Modelo de plástico de Bingham: τ = τ0 + μ_p·γ̇, para τ > τ0 (abaixo da tensão de
    escoamento τ0 o material não escoa, comporta-se como sólido — γ̇=0 nesse regime, não
    representado por esta fórmula)."""
    return tau0 + mu_plastico * taxa_deformacao


def reynolds_generalizado_lei_potencia(rho: float, v: float, D: float, K: float, n: float) -> float:
    """Número de Reynolds generalizado de Metzner-Reed, para escoamento de um fluido de lei de
    potência em tubulação circular — a extensão do número de Reynolds usual (que assume
    viscosidade newtoniana constante) para uma viscosidade aparente que depende da própria taxa
    de cisalhamento média do escoamento:

        Re' = (ρ·v^(2-n)·Dⁿ) / (8^(n-1)·K·((3n+1)/(4n))ⁿ)

    Usado no lugar de `perda_carga.numero_reynolds` para decidir o regime de escoamento (laminar
    se Re' < ~2100) e, em regime laminar, o fator de atrito de Darcy continua f = 64/Re'."""
    K_linha = K * ((3.0 * n + 1.0) / (4.0 * n)) ** n
    return (rho * v ** (2.0 - n) * D ** n) / (8.0 ** (n - 1.0) * K_linha)


def fator_atrito_laminar_lei_potencia(Re_generalizado: float) -> float:
    """Fator de atrito de Darcy em escoamento laminar de um fluido de lei de potência: mesma
    forma funcional do caso newtoniano, f = 64/Re' — mas com o Reynolds generalizado de
    Metzner-Reed (`reynolds_generalizado_lei_potencia`) no lugar do Reynolds usual. Válida só em
    regime laminar (Re' < ~2100); em regime turbulento a relação deixa de ser tão simples."""
    return 64.0 / Re_generalizado
