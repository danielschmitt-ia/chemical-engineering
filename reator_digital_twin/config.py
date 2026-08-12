"""Configuração do reator, externalizada de código para permitir reutilizar o mesmo
gêmeo digital em plantas reais diferentes só trocando o arquivo YAML — sem tocar no código
de modelagem, controle ou segurança."""

from dataclasses import dataclass, fields
from pathlib import Path

import yaml


@dataclass
class ConfiguracaoReator:
    # --- Processo ---
    V: float = 100.0          # Volume do reator (L)
    F: float = 10.0           # Vazão volumétrica (L/min)
    CA0: float = 2.0          # Concentração de entrada de A (mol/L)
    T0: float = 300.0         # Temperatura de entrada (K)
    Pre_exp_A: float = 7.2e10  # Fator pré-exponencial de Arrhenius (1/min)
    Ea_R: float = 8750.0      # Ea/R (K)
    DeltaH: float = -50000.0  # Calor de reação nominal (J/mol), usado pelo controle
    rho: float = 1000.0       # Densidade (g/L)
    Cp: float = 4.184         # Capacidade térmica (J/g·K)

    # --- Condição inicial ---
    CA_inicial: float = 2.0   # Concentração inicial de A no reator (mol/L)
    T_inicial: float = 300.0  # Temperatura inicial do reator (K)

    # --- Controle (MPC) ---
    T_alvo: float = 330.0        # Setpoint do MPC de rastreamento (K)
    T_max_seguro: float = 345.0  # Teto de temperatura imposto ao MPC (K)
    taxa_max_Tj: float = 5.0     # Limite de variação de Tj por passo de controle (K)
    Tj_min: float = 240.0        # Limite inferior do atuador (K)
    Tj_max: float = 350.0        # Limite superior do atuador (K)
    UA_nominal: float = 50000.0  # Coeficiente de troca térmica nominal (J/min·K)

    # --- Segurança (SIS) ---
    T_trip_sis: float = 320.0   # Setpoint do interlock, com margem abaixo do ponto sem retorno (K)
    Tj_seguranca: float = 240.0  # Ação do interlock: resfriamento máximo da jaqueta (K)

    # --- Economic MPC ---
    preco_produto: float = 50.0     # Receita por mol de A convertido ($/mol), ilustrativo
    custo_energia: float = 2e-5     # Custo da carga térmica da jaqueta ($/unidade de energia), ilustrativo

    # --- Identificação da planta (metadados, não usados na física) ---
    nome_planta: str = "Reator CSTR (configuração padrão)"
    tag_equipamento: str = "R-001"


def carregar_config(caminho: str | Path) -> ConfiguracaoReator:
    """Carrega uma ConfiguracaoReator de um arquivo YAML. Campos omitidos no YAML mantêm o
    valor padrão da dataclass, então um arquivo de config real só precisa listar o que muda
    em relação ao padrão."""
    caminho = Path(caminho)
    with open(caminho, "r", encoding="utf-8") as f:
        dados = yaml.safe_load(f) or {}

    campos_por_nome = {f.name: f for f in fields(ConfiguracaoReator)}
    desconhecidos = set(dados) - set(campos_por_nome)
    if desconhecidos:
        raise ValueError(f"Campos desconhecidos em {caminho}: {sorted(desconhecidos)}")

    # Notação científica sem sinal explícito no expoente (ex.: 7.2e10) é uma pegadinha
    # conhecida do PyYAML: fica como string em vez de float. Corrige silenciosamente para
    # não exigir que quem edita o YAML conheça esse detalhe da biblioteca.
    for nome, valor in list(dados.items()):
        if campos_por_nome[nome].type is float and isinstance(valor, str):
            try:
                dados[nome] = float(valor)
            except ValueError:
                raise ValueError(f"Campo '{nome}' em {caminho} deveria ser numérico, recebeu {valor!r}") from None

    return ConfiguracaoReator(**dados)
