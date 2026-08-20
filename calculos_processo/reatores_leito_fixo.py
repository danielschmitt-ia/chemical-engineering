"""Reatores de leito fixo e catalíticos: queda de pressão através do leito empacotado (equação
de Ergun) e o fator de efetividade catalítico (módulo de Thiele), que quantifica o quanto a
difusão do reagente dentro do poro do catalisador limita a taxa de reação observada frente à
taxa intrínseca (cinética pura, sem limitação difusiva).
"""

import math


def queda_pressao_ergun(v: float, dp: float, epsilon: float, rho: float, mu: float, L: float) -> float:
    """Queda de pressão através de um leito empacotado pela equação de Ergun — soma de um termo
    viscoso (domina em baixo Reynolds de partícula) e um termo inercial (domina em alto Reynolds):

        ΔP/L = 150·(1-ε)²/ε³ · (μ·v)/dp² + 1.75·(1-ε)/ε³ · (ρ·v²)/dp

    v: velocidade superficial (vazão volumétrica / área total da seção, como se o leito não
    existisse) [m/s]; dp: diâmetro da partícula [m]; epsilon (ε): porosidade do leito
    (fração de vazios, tipicamente 0.3-0.5); rho, mu: massa específica e viscosidade do fluido;
    L: comprimento do leito [m]. Retorna ΔP em Pa."""
    termo_viscoso = 150.0 * (1.0 - epsilon) ** 2 / epsilon ** 3 * (mu * v) / dp ** 2
    termo_inercial = 1.75 * (1.0 - epsilon) / epsilon ** 3 * (rho * v ** 2) / dp
    return (termo_viscoso + termo_inercial) * L


def modulo_thiele_esfera(raio_particula: float, k: float, D_efetivo: float) -> float:
    """Módulo de Thiele para uma partícula catalítica esférica e reação de primeira ordem:
    φ = R·sqrt(k/D_efetivo). R: raio da partícula [m]; k: constante de velocidade intrínseca
    [1/s]; D_efetivo: difusividade efetiva do reagente no poro do catalisador [m²/s]. φ >> 1
    indica forte limitação difusiva (reação rápida frente à difusão); φ << 1 indica regime
    cineticamente controlado (difusão rápida frente à reação)."""
    return raio_particula * math.sqrt(k / D_efetivo)


def fator_efetividade_esfera(phi: float) -> float:
    """Fator de efetividade catalítico para uma esfera e reação de primeira ordem, em função do
    módulo de Thiele (`modulo_thiele_esfera`):

        η = (3/φ²)·(φ·coth(φ) - 1)

    η=1 significa que todo o catalisador reage na taxa intrínseca (sem limitação difusiva,
    φ→0); η→0 conforme φ cresce, indicando que a reação ocorre só em uma casca fina perto da
    superfície da partícula (fortemente limitada pela difusão).

    Para φ pequeno, a forma fechada acima subtrai dois números muito próximos de 1
    (cancelamento catastrófico em ponto flutuante) — abaixo de φ=0.1 usa-se em vez disso a
    expansão em série de Taylor η ≈ 1 - φ²/15 + 2φ⁴/315, numericamente estável e com erro
    desprezível nessa faixa (< 1e-6)."""
    if phi < 0.1:
        return 1.0 - phi ** 2 / 15.0 + 2.0 * phi ** 4 / 315.0
    return (3.0 / phi ** 2) * (phi / math.tanh(phi) - 1.0)
