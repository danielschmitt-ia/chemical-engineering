"""Separação por destilação binária a volatilidade relativa constante: curva de equilíbrio,
métodos shortcut (Fenske para estágios mínimos a refluxo total, Underwood para refluxo mínimo,
Gilliland para estágios reais) e o método algébrico de McCabe-Thiele para contagem de estágios
ideais a um refluxo operacional dado.

Convenção usada em todo o módulo: `x` e `y` são frações molares do componente mais volátil
("leve") na fase líquida e vapor; `q` é a condição térmica da alimentação (1.0 = líquido
saturado, 0.0 = vapor saturado); estágios contados incluem o refletor como o último estágio de
equilíbrio (convenção padrão de Fenske/McCabe-Thiele).
"""

import math

from scipy.optimize import brentq


def volatilidade_relativa(pressao_vapor_leve: float, pressao_vapor_pesado: float) -> float:
    """Volatilidade relativa a partir das pressões de vapor puras (lei de Raoult, mistura
    ideal): α = P_sat_leve / P_sat_pesado."""
    return pressao_vapor_leve / pressao_vapor_pesado


def equilibrio_binario(x: float, alpha: float) -> float:
    """Composição do vapor em equilíbrio com um líquido de composição `x`, para volatilidade
    relativa constante: y = αx / (1 + (α-1)x)."""
    return alpha * x / (1.0 + (alpha - 1.0) * x)


def composicao_liquido_equilibrio(y: float, alpha: float) -> float:
    """Inversa de `equilibrio_binario`: composição do líquido em equilíbrio com um vapor de
    composição `y`, x = y / (α - (α-1)y)."""
    return y / (alpha - (alpha - 1.0) * y)


def numero_minimo_estagios_fenske(xD: float, xB: float, alpha: float) -> float:
    """Equação de Fenske: número mínimo de estágios de equilíbrio (incluindo o refervedor) para
    atingir as composições de topo `xD` e fundo `xB` desejadas, no limite de refluxo total
    (razão de refluxo infinita):

        N_min = ln[(xD/(1-xD))·((1-xB)/xB)] / ln(α)

    Usa `alpha` constante (aproximação usual quando a volatilidade relativa varia pouco entre
    o topo e o fundo da coluna; para variações grandes, usar a média geométrica de α no topo e
    no fundo)."""
    return math.log((xD / (1.0 - xD)) * ((1.0 - xB) / xB)) / math.log(alpha)


def refluxo_minimo(xD: float, xF: float, alpha: float, q: float = 1.0) -> float:
    """Razão de refluxo mínima (método de Underwood, caso de volatilidade relativa constante):
    no refluxo mínimo, as linhas de operação se encontram exatamente sobre a curva de
    equilíbrio no ponto de alimentação — um "pinch" de estágios infinitos. Encontra esse ponto
    de pinch (interseção da reta q com a curva de equilíbrio) e calcula:

        R_min = (xD - y_pinch) / (y_pinch - x_pinch)

    Para alimentação líquido saturado (q=1, caso mais comum), a reta q é vertical em x=xF e o
    pinch é simplesmente (xF, y_eq(xF)) — resolvido em forma fechada. Para outros `q`, a
    interseção é obtida numericamente (a reta q intersecta a curva de equilíbrio racional em
    dois pontos possíveis; busca-se a raiz fisicamente relevante em (0, 1))."""
    if math.isclose(q, 1.0, abs_tol=1e-9):
        x_pinch = xF
    else:
        def reta_q(x: float) -> float:
            return q / (q - 1.0) * x - xF / (q - 1.0)

        def diferenca(x: float) -> float:
            return reta_q(x) - equilibrio_binario(x, alpha)

        x_pinch = brentq(diferenca, 1e-9, 1.0 - 1e-9)
    y_pinch = equilibrio_binario(x_pinch, alpha)
    return (xD - y_pinch) / (y_pinch - x_pinch)


def estagios_gilliland(N_min: float, R_min: float, R: float) -> float:
    """Correlação de Gilliland (aproximação explícita de Eduljee, 1975) para estimar o número
    real de estágios de equilíbrio N a um refluxo operacional R > R_min, a partir do número
    mínimo de estágios (Fenske) e do refluxo mínimo (Underwood) — evita ter que rodar o
    stepping de McCabe-Thiele quando só se quer uma estimativa rápida:

        X = (R - R_min)/(R + 1)
        Y = 1 - exp{[(1 + 54.4X)/(11 + 117.2X)]·[(X-1)/√X]}
        N = (Y + N_min)/(1 - Y)
    """
    if R <= R_min:
        raise ValueError("R precisa ser maior que R_min para a coluna ser factível")
    X = (R - R_min) / (R + 1.0)
    Y = 1.0 - math.exp(((1.0 + 54.4 * X) / (11.0 + 117.2 * X)) * ((X - 1.0) / math.sqrt(X)))
    return (Y + N_min) / (1.0 - Y)


def estagios_mccabe_thiele(xD: float, xB: float, xF: float, alpha: float, R: float, q: float = 1.0,
                            max_estagios: int = 200) -> tuple[int, list[tuple[float, float]]]:
    """Contagem de estágios ideais pelo método algébrico de McCabe-Thiele (equivalente ao
    stepping gráfico clássico, sem depender de um gráfico): degraus alternados entre a curva de
    equilíbrio e as retas de operação, partindo do topo (xD, xD) até atingir xB.

    Reta de retificação (acima da alimentação): y = R/(R+1)·x + xD/(R+1).
    Ponto de troca de reta: interseção entre a reta de retificação e a reta q (mesma construção
    geométrica do método gráfico — o ponto onde a alimentação entra na coluna).
    Reta de esgotamento (abaixo da alimentação): reta que liga esse ponto de interseção a
    (xB, xB), pela definição do balanço de massa na seção de esgotamento.

    Retorna `(numero_de_estagios, pontos)`, com `pontos` a sequência de vértices (x, y) visitados
    — útil para reproduzir o diagrama de McCabe-Thiele em um gráfico. O refervedor é contado
    como o último estágio de equilíbrio (mesma convenção de `numero_minimo_estagios_fenske`)."""
    if not xB < xF < xD:
        raise ValueError("É necessário xB < xF < xD")

    def y_retificacao(x: float) -> float:
        return R / (R + 1.0) * x + xD / (R + 1.0)

    if math.isclose(q, 1.0, abs_tol=1e-9):
        x_i = xF
    else:
        a = R / (R + 1.0) - q / (q - 1.0)
        b = -xF / (q - 1.0) - xD / (R + 1.0)
        x_i = b / a
    y_i = y_retificacao(x_i)

    if math.isclose(x_i, xB, abs_tol=1e-12):
        raise ValueError("Ponto de interseção coincide com xB — verifique xF e q")
    inclinacao_esgotamento = (y_i - xB) / (x_i - xB)

    def y_esgotamento(x: float) -> float:
        return inclinacao_esgotamento * (x - xB) + xB

    pontos = [(xD, xD)]
    x_atual, y_atual = xD, xD
    n_estagios = 0
    for _ in range(max_estagios):
        x_atual = composicao_liquido_equilibrio(y_atual, alpha)
        n_estagios += 1
        pontos.append((x_atual, y_atual))
        if x_atual <= xB:
            return n_estagios, pontos

        y_atual = y_retificacao(x_atual) if x_atual > x_i else y_esgotamento(x_atual)
        pontos.append((x_atual, y_atual))

    raise RuntimeError(f"Não convergiu para xB em {max_estagios} estágios — verifique R > R_min")
