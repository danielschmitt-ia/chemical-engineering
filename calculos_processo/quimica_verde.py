"""Química verde: economia atômica (atom economy, Trost 1991) — a métrica que mede, pela própria
estequiometria da reação, que fração da massa dos reagentes termina incorporada no produto
desejado, antes mesmo de considerar rendimento real de processo. Uma das métricas centrais dos 12
princípios da química verde (prevenção de resíduo já embutida na escolha da rota de síntese)."""

from collections.abc import Sequence


def economia_atomica(massa_molar_produto: float, coeficiente_produto: float,
                      massas_molares_reagentes: Sequence[float], coeficientes_reagentes: Sequence[float]) -> float:
    """Economia atômica de uma rota de síntese, pela estequiometria balanceada da reação:

        AE = (coef_produto·M_produto) / Σ(coef_reagente_i·M_reagente_i)

    Diferente do rendimento de processo (`conversao.rendimento_a_partir_de_mols`), a economia
    atômica é uma propriedade da própria equação química balanceada — não depende de quão bem a
    reação de fato ocorre, só de quanto da massa dos reagentes tem, no melhor caso possível,
    chance de acabar no produto desejado. Uma reação de adição (ex.: hidrogenação) tende a AE
    próxima de 1 (nenhum átomo "sobra" fora do produto); uma reação de substituição com
    subproduto pesado (ex.: um sal formado como coproduto) tende a AE baixa, mesmo com
    rendimento de processo de 100%. Retorna uma fração (0-1)."""
    massa_produto = coeficiente_produto * massa_molar_produto
    massa_reagentes = sum(c * m for c, m in zip(coeficientes_reagentes, massas_molares_reagentes))
    return massa_produto / massa_reagentes
