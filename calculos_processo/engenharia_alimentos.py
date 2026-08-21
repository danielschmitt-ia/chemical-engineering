"""Engenharia de alimentos e bioprocessos — processamento térmico (pasteurização/esterilização):
cinética de morte térmica microbiana de primeira ordem (valores D e z, taxa letal) e a letalidade
acumulada de um perfil tempo-temperatura real (F0), a base do método de Bigelow/Ball usado para
validar ciclos de esterilização.
"""

import numpy as np


def taxa_letal(T: float, T_ref: float, z: float) -> float:
    """Taxa letal na temperatura T, relativa à temperatura de referência T_ref: L = 10^((T-T_ref)/z).
    L=1 na temperatura de referência; L cresce 10x a cada `z` graus acima dela — é o fator pelo
    qual a velocidade de morte microbiana (ou de degradação de nutrientes) aumenta com a
    temperatura, segundo o modelo de primeira ordem clássico do processamento térmico. Mesma
    unidade de temperatura em T, T_ref e z (°C mais comum na literatura de alimentos)."""
    return 10.0 ** ((T - T_ref) / z)


def valor_D_na_temperatura(D_ref: float, T: float, T_ref: float, z: float) -> float:
    """Valor D (tempo para reduzir a população microbiana em 1 ciclo log, 90%) na temperatura T,
    a partir do valor D conhecido na temperatura de referência: D(T) = D_ref · 10^(-(T-T_ref)/z)
    — inversamente proporcional à taxa letal, já que uma taxa letal maior reduz o tempo
    necessário para a mesma redução logarítmica."""
    return D_ref * 10.0 ** (-(T - T_ref) / z)


def letalidade_acumulada(tempos: np.ndarray, temperaturas: np.ndarray, T_ref: float, z: float) -> float:
    """Letalidade acumulada (F0) de um perfil tempo-temperatura real, medido ou simulado durante
    um processo térmico: F0 = ∫ 10^((T(t)-T_ref)/z) dt, integrada numericamente (regra do
    trapézio) sobre os pontos amostrados. `tempos` na mesma unidade em que F0 deve ser expresso
    (min é o padrão na literatura de esterilização); `temperaturas` na mesma unidade de T_ref."""
    taxa = 10.0 ** ((np.asarray(temperaturas) - T_ref) / z)
    return float(np.trapz(taxa, np.asarray(tempos)))


def reducoes_logaritmicas(F0: float, D_ref: float) -> float:
    """Número de reduções logarítmicas (ciclos log) de população microbiana obtidas por uma
    letalidade acumulada F0, na temperatura de referência de D_ref: n = F0/D_ref."""
    return F0 / D_ref


def populacao_sobrevivente(N0: float, reducoes_log: float) -> float:
    """População microbiana sobrevivente após `reducoes_log` reduções logarítmicas a partir de
    uma população inicial N0: N = N0 · 10^(-reducoes_log)."""
    return N0 * 10.0 ** (-reducoes_log)
