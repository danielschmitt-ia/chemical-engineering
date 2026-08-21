"""Perda de carga (queda de pressão por atrito) em escoamento interno em tubulações —
equação de Darcy-Weisbach, com fator de atrito de Darcy calculado via correlação explícita de
Swamee-Jain (evita a natureza implícita da equação de Colebrook-White) e perdas localizadas em
acessórios (válvulas, curvas, tês) pelo método do coeficiente de resistência K.
"""

import math


def numero_reynolds(rho: float, v: float, D: float, mu: float) -> float:
    """Número de Reynolds do escoamento: Re = ρ·v·D/μ.

    rho: massa específica do fluido (kg/m³); v: velocidade média (m/s);
    D: diâmetro interno da tubulação (m); mu: viscosidade dinâmica (Pa·s)."""
    return rho * v * D / mu


def velocidade_escoamento(vazao_volumetrica: float, D: float) -> float:
    """Velocidade média do escoamento a partir da vazão volumétrica (m³/s) e do diâmetro
    interno da tubulação (m): v = Q/A, com A = πD²/4."""
    area = math.pi * D ** 2 / 4
    return vazao_volumetrica / area


def fator_atrito_darcy(Re: float, rugosidade_relativa: float = 0.0) -> float:
    """Fator de atrito de Darcy, usado na equação de Darcy-Weisbach.

    Regime laminar (Re <= 2300): solução exata f = 64/Re.
    Regime turbulento (Re > 2300): correlação explícita de Swamee-Jain, uma aproximação da
    equação implícita de Colebrook-White com erro tipicamente < 1%, evitando iteração:
        f = 0.25 / [log10(rugosidade_relativa/3.7 + 5.74/Re^0.9)]²
    Formalmente válida para Re entre 5000 e 1e8 e rugosidade relativa entre 1e-6 e 1e-2; usada
    aqui também na faixa de transição (2300-5000) como aproximação de engenharia, prática comum
    quando não há necessidade de precisão de projeto detalhado nessa faixa estreita."""
    if Re <= 0:
        raise ValueError("Reynolds precisa ser positivo")
    if Re <= 2300:
        return 64.0 / Re
    return 0.25 / (math.log10(rugosidade_relativa / 3.7 + 5.74 / Re ** 0.9)) ** 2


def perda_carga_distribuida(f: float, L: float, D: float, rho: float, v: float) -> float:
    """Perda de carga distribuída (atrito ao longo do trecho reto) pela equação de
    Darcy-Weisbach: ΔP = f·(L/D)·(ρv²/2) [Pa]. L e D em metros, rho em kg/m³, v em m/s."""
    return f * (L / D) * (rho * v ** 2 / 2)


def perda_carga_localizada(K_total: float, rho: float, v: float) -> float:
    """Perda de carga localizada (acessórios: válvulas, curvas, tês, reduções) pelo método do
    coeficiente de resistência: ΔP = K_total·(ρv²/2) [Pa]. `K_total` é a soma dos coeficientes K
    de cada acessório no trecho."""
    return K_total * (rho * v ** 2 / 2)


def perda_carga_total(vazao_volumetrica: float, D: float, L: float, rho: float, mu: float,
                       rugosidade_absoluta: float = 0.0, K_total: float = 0.0) -> dict:
    """Perda de carga total em um trecho de tubulação (distribuída + localizada), calculando
    internamente velocidade, Reynolds e fator de atrito. Retorna um dict com todas as grandezas
    intermediárias, útil tanto para obter o resultado final quanto para auditar o cálculo:
    `{"velocidade", "reynolds", "fator_atrito", "delta_p_distribuida", "delta_p_localizada",
    "delta_p_total"}` (Pa, exceto velocidade em m/s e reynolds adimensional)."""
    v = velocidade_escoamento(vazao_volumetrica, D)
    Re = numero_reynolds(rho, v, D, mu)
    f = fator_atrito_darcy(Re, rugosidade_absoluta / D)
    dp_distribuida = perda_carga_distribuida(f, L, D, rho, v)
    dp_localizada = perda_carga_localizada(K_total, rho, v)
    return {
        "velocidade": v,
        "reynolds": Re,
        "fator_atrito": f,
        "delta_p_distribuida": dp_distribuida,
        "delta_p_localizada": dp_localizada,
        "delta_p_total": dp_distribuida + dp_localizada,
    }
