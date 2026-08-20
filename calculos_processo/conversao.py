"""Conversão de reagentes em reações químicas: conversão, reagente limitante, grau de avanço
(extensão de reação) e as métricas de desempenho que dependem dele — seletividade e rendimento
— para reações com subprodutos.
"""

from collections.abc import Mapping


def conversao(quantidade_inicial: float, quantidade_final: float) -> float:
    """Conversão de um reagente: fração da quantidade inicial que foi consumida,
    X = (n0 - n)/n0. Aceita mols, concentração ou vazão molar (regime permanente, mesma base em
    ambos os argumentos) — a fórmula é a mesma nos três casos."""
    if quantidade_inicial <= 0:
        raise ValueError("quantidade_inicial precisa ser positiva")
    return (quantidade_inicial - quantidade_final) / quantidade_inicial


def quantidade_final_a_partir_conversao(quantidade_inicial: float, X: float) -> float:
    """Inversa de `conversao`: quantidade restante do reagente dada a conversão X, n = n0(1-X)."""
    return quantidade_inicial * (1.0 - X)


def reagente_limitante(mols_disponiveis: Mapping[str, float], coeficientes_estequiometricos: Mapping[str, float]) -> str:
    """Identifica o reagente limitante de uma reação, dados os mols disponíveis de cada
    reagente e o valor absoluto de seu coeficiente estequiométrico (ex.: para
    A + 3B -> produtos, `coeficientes_estequiometricos = {"A": 1, "B": 3}`).

    O limitante é o reagente com a menor razão mols_disponíveis/coeficiente — o primeiro a se
    esgotar se a reação prosseguir até o fim, mesmo que não seja o de menor quantidade em mols
    (um reagente com coeficiente estequiométrico alto se esgota mais rápido por mol
    disponível)."""
    if set(mols_disponiveis) != set(coeficientes_estequiometricos):
        raise ValueError("mols_disponiveis e coeficientes_estequiometricos devem ter os mesmos reagentes")
    razoes = {reagente: mols_disponiveis[reagente] / coeficientes_estequiometricos[reagente]
              for reagente in mols_disponiveis}
    return min(razoes, key=razoes.get)


def grau_avanco(mols_inicial: float, mols_final: float, coeficiente_estequiometrico: float) -> float:
    """Grau de avanço (extensão) da reação, ξ = (n - n0)/ν. `coeficiente_estequiometrico` (ν) é
    negativo para reagentes e positivo para produtos, na convenção usual de estequiometria
    (ex.: para A + 3B -> 2C, ν_A=-1, ν_B=-3, ν_C=2) — com essa convenção, ξ é sempre >= 0
    conforme a reação avança, seja a espécie usada para calculá-lo um reagente ou um produto."""
    if coeficiente_estequiometrico == 0:
        raise ValueError("coeficiente_estequiometrico não pode ser zero")
    return (mols_final - mols_inicial) / coeficiente_estequiometrico


def mols_a_partir_avanco(mols_inicial: float, coeficiente_estequiometrico: float, avanco: float) -> float:
    """Inversa de `grau_avanco`: mols de uma espécie dado o grau de avanço ξ da reação,
    n = n0 + ν·ξ (mesma convenção de sinais de `grau_avanco`)."""
    return mols_inicial + coeficiente_estequiometrico * avanco


def seletividade(mols_produto_desejado: float, mols_produto_indesejado: float) -> float:
    """Seletividade do produto desejado frente ao(s) indesejado(s): razão entre os mols
    formados de cada um. Usada junto com a conversão para compor o rendimento global em
    reações com subprodutos."""
    if mols_produto_indesejado == 0:
        # Nenhum subproduto formado: seletividade perfeita (+inf), a menos que também não
        # tenha se formado produto desejado (reação ainda não ocorreu) — nesse caso, 0/0 é
        # indefinido e tratado como 0.
        return float("inf") if mols_produto_desejado > 0 else 0.0
    return mols_produto_desejado / mols_produto_indesejado


def rendimento_global(X: float, S: float) -> float:
    """Rendimento global do produto desejado em relação ao reagente-base: Y = X·S (conversão
    vezes seletividade). Representa a fração do reagente alimentado que efetivamente vira
    produto desejado — a métrica que combina "quanto reagiu" com "quão bem direcionado" foi."""
    return X * S


def rendimento_a_partir_de_mols(mols_produto_obtido: float, mols_produto_teorico_maximo: float) -> float:
    """Rendimento a partir de mols medidos: Y = mols_obtido / mols_teórico_máximo, onde o
    teórico máximo é o que se obteria com conversão total do reagente limitante e seletividade
    perfeita (100%) para o produto desejado, segundo a estequiometria da reação."""
    if mols_produto_teorico_maximo <= 0:
        raise ValueError("mols_produto_teorico_maximo precisa ser positivo")
    return mols_produto_obtido / mols_produto_teorico_maximo
