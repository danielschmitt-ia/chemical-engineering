"""Ferramentas de cálculo de engenharia de processos químicos — independentes do gêmeo digital
do reator (`reator_digital_twin/`), mas usadas no mesmo tipo de análise de fluxograma: balanço
de massa e energia, termodinâmica química, mecânica dos fluidos, reologia não-newtoniana,
tubulações industriais, perda de carga, transferência de calor, separação por destilação,
conversão de reagentes e composição de misturas (fração molar/mássica)."""

from .balanco_energia import (
    balanco_energia_escoamento,
    energia_cinetica_especifica,
    energia_potencial_especifica,
    residuo_balanco_energia_global,
)
from .balanco_massa import divisor, misturador, residuo_balanco_massa_global, vazao_desconhecida
from .bioreatores import (
    biomassa_crescimento_exponencial,
    rendimento_biomassa_substrato,
    taxa_especifica_crescimento_monod,
    taxa_transferencia_oxigenio,
    tempo_duplicacao,
)
from .cinetica_reatores import (
    conversao_cstr_primeira_ordem,
    conversao_pfr_primeira_ordem,
    constante_velocidade_arrhenius,
    numero_damkohler,
    taxa_reacao_ordem_n,
    tempo_batelada,
    tempo_espacial_cstr,
    tempo_espacial_pfr,
)
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
from .eletroquimica import (
    eficiencia_corrente,
    massa_produzida_faraday,
    mols_produzidos_faraday,
    potencial_nernst,
    tempo_necessario_faraday,
)
from .engenharia_alimentos import (
    letalidade_acumulada,
    populacao_sobrevivente,
    reducoes_logaritmicas,
    taxa_letal,
    valor_D_na_temperatura,
)
from .destilacao import (
    composicao_liquido_equilibrio,
    equilibrio_binario,
    estagios_gilliland,
    estagios_mccabe_thiele,
    numero_minimo_estagios_fenske,
    refluxo_minimo,
    volatilidade_relativa,
)
from .fluidizacao import (
    numero_arquimedes,
    queda_pressao_leito_fluidizado,
    velocidade_minima_fluidizacao,
)
from .fracao_molar import (
    fracao_massica_a_partir_molar,
    fracao_molar_a_partir_massica,
    massa_molar_media,
    pressao_parcial,
)
from .mecanica_fluidos import (
    numero_reynolds_particula,
    potencia_eixo_bomba,
    potencia_hidraulica_bomba,
    trabalho_bomba_necessario,
    velocidade_terminal_stokes,
)
from .perda_carga import (
    fator_atrito_darcy,
    numero_reynolds,
    perda_carga_distribuida,
    perda_carga_localizada,
    perda_carga_total,
    velocidade_escoamento,
)
from .piping import (
    diametro_a_partir_de_velocidade,
    dilatacao_termica_tubulacao,
    espessura_minima_parede,
    tensao_admissivel_expansao_termica,
)
from .reatores_leito_fixo import (
    fator_efetividade_esfera,
    modulo_thiele_esfera,
    queda_pressao_ergun,
)
from .reologia import (
    fator_atrito_laminar_lei_potencia,
    reynolds_generalizado_lei_potencia,
    tensao_cisalhante_bingham,
    tensao_cisalhante_lei_potencia,
    viscosidade_aparente_lei_potencia,
)
from .termodinamica import (
    clausius_clapeyron_pressao,
    constante_equilibrio,
    energia_livre_gibbs_reacao,
    fator_compressibilidade,
    pressao_gas_ideal,
    pressao_vapor_antoine,
    temperatura_ebulicao_antoine,
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
    # balanco_energia
    "balanco_energia_escoamento",
    "energia_cinetica_especifica",
    "energia_potencial_especifica",
    "residuo_balanco_energia_global",
    # balanco_massa
    "divisor",
    "misturador",
    "residuo_balanco_massa_global",
    "vazao_desconhecida",
    # cinetica_reatores
    "constante_velocidade_arrhenius",
    "conversao_cstr_primeira_ordem",
    "conversao_pfr_primeira_ordem",
    "numero_damkohler",
    "taxa_reacao_ordem_n",
    "tempo_batelada",
    "tempo_espacial_cstr",
    "tempo_espacial_pfr",
    # engenharia_alimentos
    "letalidade_acumulada",
    "populacao_sobrevivente",
    "reducoes_logaritmicas",
    "taxa_letal",
    "valor_D_na_temperatura",
    # reatores_leito_fixo
    "fator_efetividade_esfera",
    "modulo_thiele_esfera",
    "queda_pressao_ergun",
    # fluidizacao
    "numero_arquimedes",
    "queda_pressao_leito_fluidizado",
    "velocidade_minima_fluidizacao",
    # bioreatores
    "biomassa_crescimento_exponencial",
    "rendimento_biomassa_substrato",
    "taxa_especifica_crescimento_monod",
    "taxa_transferencia_oxigenio",
    "tempo_duplicacao",
    # eletroquimica
    "eficiencia_corrente",
    "massa_produzida_faraday",
    "mols_produzidos_faraday",
    "potencial_nernst",
    "tempo_necessario_faraday",
    # mecanica_fluidos
    "numero_reynolds_particula",
    "potencia_eixo_bomba",
    "potencia_hidraulica_bomba",
    "trabalho_bomba_necessario",
    "velocidade_terminal_stokes",
    # piping
    "diametro_a_partir_de_velocidade",
    "dilatacao_termica_tubulacao",
    "espessura_minima_parede",
    "tensao_admissivel_expansao_termica",
    # reologia
    "fator_atrito_laminar_lei_potencia",
    "reynolds_generalizado_lei_potencia",
    "tensao_cisalhante_bingham",
    "tensao_cisalhante_lei_potencia",
    "viscosidade_aparente_lei_potencia",
    # termodinamica
    "clausius_clapeyron_pressao",
    "constante_equilibrio",
    "energia_livre_gibbs_reacao",
    "fator_compressibilidade",
    "pressao_gas_ideal",
    "pressao_vapor_antoine",
    "temperatura_ebulicao_antoine",
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
