"""Análise financeira de projetos: valor presente líquido (VPL/NPV), payback simples e taxa
interna de retorno (TIR/IRR) — os três critérios clássicos de avaliação de viabilidade econômica
de um projeto de investimento, cada um respondendo uma pergunta ligeiramente diferente (VPL: o
projeto cria valor? payback: em quanto tempo o investimento se recupera? TIR: qual taxa de
retorno o projeto entrega?)."""

from collections.abc import Sequence

from scipy.optimize import brentq


def valor_presente_liquido(fluxos_caixa: Sequence[float], taxa_desconto: float) -> float:
    """Valor presente líquido (VPL/NPV): VPL = Σ FC_t/(1+r)^t, para t=0,1,...,n. `fluxos_caixa`
    é a série completa, começando pelo investimento inicial em t=0 (tipicamente negativo);
    `taxa_desconto` (r) é a taxa mínima de atratividade (custo de capital) do investidor, como
    fração (ex.: 0.12 para 12% a.a.). VPL > 0 indica que o projeto cria valor acima do custo de
    capital; VPL < 0, que destrói valor mesmo que o fluxo de caixa nominal total seja positivo."""
    return sum(fc / (1.0 + taxa_desconto) ** t for t, fc in enumerate(fluxos_caixa))


def payback_simples(investimento_inicial: float, fluxo_caixa_anual: float) -> float:
    """Payback simples (não descontado), para um fluxo de caixa anual uniforme após o
    investimento inicial: payback = investimento_inicial/fluxo_caixa_anual — o tempo para o
    fluxo de caixa acumulado igualar o investimento. Não considera o valor do dinheiro no tempo
    (ao contrário do VPL) nem o que acontece depois do payback — um critério simples de triagem
    inicial, não de decisão final de investimento."""
    return investimento_inicial / fluxo_caixa_anual


def taxa_interna_retorno(fluxos_caixa: Sequence[float], chute_inferior: float = -0.99,
                          chute_superior: float = 10.0) -> float:
    """Taxa interna de retorno (TIR/IRR): a taxa de desconto r para a qual VPL(r) = 0 — a taxa de
    retorno que o próprio projeto entrega, comparável diretamente contra o custo de capital do
    investidor (projeto viável se TIR > custo de capital, o mesmo critério de VPL > 0 avaliado à
    taxa de custo de capital). Encontrada numericamente (`scipy.optimize.brentq`) — só bem
    definida (raiz única) para o padrão convencional de fluxo de caixa (um investimento inicial
    negativo seguido só de fluxos positivos); múltiplas trocas de sinal no fluxo de caixa podem
    produzir múltiplas TIRs matematicamente válidas, um cenário fora do escopo desta função.
    Levanta `ValueError` (propagado do `brentq`) se não houver troca de sinal de VPL no intervalo
    de busca `[chute_inferior, chute_superior]`."""
    return brentq(lambda r: valor_presente_liquido(fluxos_caixa, r), chute_inferior, chute_superior)
