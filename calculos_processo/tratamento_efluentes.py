"""Tratamento de efluentes e gestão ambiental: eficiência de remoção de um poluente e a carga
poluente (mass loading) de uma corrente — as duas métricas mais básicas para dimensionar e
reportar o desempenho de qualquer etapa de tratamento (biológico, físico-químico)."""


def eficiencia_remocao(concentracao_entrada: float, concentracao_saida: float) -> float:
    """Eficiência de remoção de um poluente: η = (C_entrada - C_saída)/C_entrada. Mesma unidade
    de concentração em ambas (ex.: DBO, DQO, sólidos suspensos totais — mg/L). Retorna uma fração
    (0-1); multiplique por 100 para porcentagem."""
    return (concentracao_entrada - concentracao_saida) / concentracao_entrada


def carga_poluente(vazao: float, concentracao: float) -> float:
    """Carga poluente (mass loading rate): massa de poluente por unidade de tempo — L = Q·C. A
    grandeza usada para dimensionar um tratamento (ex.: carga orgânica de um reator biológico) e
    para reporte regulatório de emissões, em vez da concentração isolada (que não captura o
    volume total tratado)."""
    return vazao * concentracao
