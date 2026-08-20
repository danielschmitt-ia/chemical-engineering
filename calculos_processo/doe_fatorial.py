"""Design de Experimentos (DoE): dimensionamento de um planejamento fatorial completo e cálculo
do efeito principal de um fator — as duas contas mais básicas antes de rodar um DoE, mesmo que a
análise estatística completa (ANOVA, superfícies de resposta) fique fora do escopo deste módulo.
"""

from collections.abc import Sequence


def numero_ensaios_fatorial(k: int, niveis: int = 2, replicas: int = 1) -> int:
    """Número de ensaios de um planejamento fatorial completo: níveis^k · réplicas. `k`: número
    de fatores estudados; `niveis`: número de níveis testados por fator (2 é o caso mais comum —
    fatorial 2^k, usado para triagem e estimativa de efeitos principais/interações lineares);
    `replicas`: repetições de cada combinação, para estimar o erro experimental."""
    return niveis ** k * replicas


def efeito_principal(respostas_nivel_alto: Sequence[float], respostas_nivel_baixo: Sequence[float]) -> float:
    """Efeito principal de um fator em um planejamento fatorial 2^k: a diferença entre a média
    das respostas em todos os ensaios com o fator no nível alto e a média das respostas com o
    fator no nível baixo — quanto, em média, a resposta muda ao mover esse fator do nível baixo
    para o alto, marginalizando sobre todos os outros fatores. Um efeito grande frente ao erro
    experimental (estimado pelas réplicas) indica um fator que importa; um efeito próximo de
    zero, um fator que pode ser removido do modelo."""
    media_alto = sum(respostas_nivel_alto) / len(respostas_nivel_alto)
    media_baixo = sum(respostas_nivel_baixo) / len(respostas_nivel_baixo)
    return media_alto - media_baixo
