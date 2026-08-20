"""Ferramentas de cálculo de engenharia de processos químicos — independentes do gêmeo digital
do reator (`reator_digital_twin/`), mas usadas no mesmo tipo de análise de fluxograma: balanço
de massa, perda de carga em tubulações, transferência de calor, separação por destilação,
conversão de reagentes e composição de misturas (fração molar/mássica)."""

from .balanco_massa import divisor, misturador, residuo_balanco_massa_global, vazao_desconhecida
from .conversao import (
    grau_avanco,
    mols_a_partir_avanco,
    quantidade_final_a_partir_conversao,
    reagente_limitante,
    rendimento_a_partir_de_mols,
    rendimento_global,
    seletividade,
)
from .conversao import conversao as conversao_reagente
from .destilacao import (
    composicao_liquido_equilibrio,
    equilibrio_binario,
    estagios_gilliland,
    estagios_mccabe_thiele,
    numero_minimo_estagios_fenske,
    refluxo_minimo,
    volatilidade_relativa,
)
from .fracao_molar import (
    fracao_massica_a_partir_molar,
    fracao_molar_a_partir_massica,
    massa_molar_media,
    pressao_parcial,
)
from .perda_carga import (
    fator_atrito_darcy,
    numero_reynolds,
    perda_carga_distribuida,
    perda_carga_localizada,
    perda_carga_total,
    velocidade_escoamento,
)
from .transferencia_calor import (
    area_troca_termica,
    calor_sensivel,
    coeficiente_global_troca,
    diferenca_temperatura_media_log,
    dtml_trocador,
    taxa_calor_trocador,
)

__all__ = [
    # balanco_massa
    "divisor",
    "misturador",
    "residuo_balanco_massa_global",
    "vazao_desconhecida",
    # perda_carga
    "fator_atrito_darcy",
    "numero_reynolds",
    "perda_carga_distribuida",
    "perda_carga_localizada",
    "perda_carga_total",
    "velocidade_escoamento",
    # transferencia_calor
    "area_troca_termica",
    "calor_sensivel",
    "coeficiente_global_troca",
    "diferenca_temperatura_media_log",
    "dtml_trocador",
    "taxa_calor_trocador",
    # destilacao
    "composicao_liquido_equilibrio",
    "equilibrio_binario",
    "estagios_gilliland",
    "estagios_mccabe_thiele",
    "numero_minimo_estagios_fenske",
    "refluxo_minimo",
    "volatilidade_relativa",
    # conversao
    "conversao_reagente",
    "grau_avanco",
    "mols_a_partir_avanco",
    "quantidade_final_a_partir_conversao",
    "reagente_limitante",
    "rendimento_a_partir_de_mols",
    "rendimento_global",
    "seletividade",
    # fracao_molar
    "fracao_massica_a_partir_molar",
    "fracao_molar_a_partir_massica",
    "massa_molar_media",
    "pressao_parcial",
]
