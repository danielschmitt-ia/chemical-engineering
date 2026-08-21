"""Balanço de massa em processos: fechamento de balanço global, misturadores e divisores
de corrente (splitters) — as operações unitárias não-reativas mais comuns em fluxogramas de
processo. Balanços que envolvem reação química (grau de avanço, reagente limitante) ficam em
`conversao.py`, já que dependem da estequiometria da reação, não só de conservação de massa.
"""

from collections.abc import Sequence


def vazao_desconhecida(vazoes_entrada: Sequence[float | None], vazoes_saida: Sequence[float | None]) -> float:
    """Resolve a única vazão desconhecida (marcada com `None`) em um balanço de massa global
    em regime permanente, sem reação: soma das entradas = soma das saídas. Útil para fechar o
    balanço de um equipamento (misturador, vaso, trocador) quando todas as correntes menos uma
    foram medidas."""
    entrada = list(vazoes_entrada)
    saida = list(vazoes_saida)
    desconhecidos = entrada.count(None) + saida.count(None)
    if desconhecidos != 1:
        raise ValueError(f"Balanço precisa de exatamente 1 vazão desconhecida (None), recebeu {desconhecidos}")

    soma_entrada_conhecida = sum(v for v in entrada if v is not None)
    soma_saida_conhecida = sum(v for v in saida if v is not None)
    if None in entrada:
        # soma_entrada_conhecida + x = soma_saida_conhecida
        return soma_saida_conhecida - soma_entrada_conhecida
    # soma_entrada_conhecida = soma_saida_conhecida + x
    return soma_entrada_conhecida - soma_saida_conhecida


def residuo_balanco_massa_global(vazoes_entrada: Sequence[float], vazoes_saida: Sequence[float]) -> float:
    """Resíduo do balanço de massa global em regime permanente (entrada - saída). Um resíduo
    != 0 indica acúmulo (regime transiente), reação com variação de massa total (rara — a massa
    total se conserva mesmo com reação química) ou, na prática, erro de medição/instrumentação —
    o uso típico é reconciliação de dados de planta, comparando o resíduo com a incerteza
    esperada dos medidores de vazão."""
    return sum(vazoes_entrada) - sum(vazoes_saida)


def misturador(correntes: Sequence[tuple[float, dict[str, float]]]) -> tuple[float, dict[str, float]]:
    """Balanço de massa em um misturador (várias correntes de entrada, uma de saída).

    `correntes` é uma lista de `(vazao_massica, fracoes_massicas)`, onde `fracoes_massicas` é
    um dict `{componente: fracao}` que deve somar 1 em cada corrente de entrada. Retorna
    `(vazao_total, fracoes_massicas_mistura)`: a vazão de saída é a soma das entradas (não há
    reação nem acúmulo) e a composição da mistura é a média ponderada pela vazão de cada
    componente."""
    if not correntes:
        raise ValueError("Precisa de ao menos uma corrente de entrada")

    vazao_total = sum(vazao for vazao, _ in correntes)
    if vazao_total <= 0:
        raise ValueError("Vazão total precisa ser positiva")

    massa_por_componente: dict[str, float] = {}
    for vazao, fracoes in correntes:
        for componente, fracao in fracoes.items():
            massa_por_componente[componente] = massa_por_componente.get(componente, 0.0) + vazao * fracao

    fracoes_mistura = {componente: massa / vazao_total for componente, massa in massa_por_componente.items()}
    return vazao_total, fracoes_mistura


def divisor(vazao_entrada: float, fracoes_divisao: dict[str, float], tol: float = 1e-6) -> dict[str, float]:
    """Balanço de massa em um divisor de corrente (splitter): uma entrada, várias saídas com a
    mesma composição da entrada, distribuída segundo `fracoes_divisao` (ex.: `{"reciclo": 0.3,
    "purga": 0.7}`). As frações precisam somar 1 — um splitter não cria nem destrói massa."""
    soma_fracoes = sum(fracoes_divisao.values())
    if abs(soma_fracoes - 1.0) > tol:
        raise ValueError(f"Frações de divisão devem somar 1, somaram {soma_fracoes}")
    return {saida: vazao_entrada * fracao for saida, fracao in fracoes_divisao.items()}
