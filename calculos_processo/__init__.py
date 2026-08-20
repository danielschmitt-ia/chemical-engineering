"""Ferramentas de cálculo de engenharia de processos químicos — independentes do gêmeo digital
do reator (`reator_digital_twin/`), mas usadas no mesmo tipo de análise de fluxograma: balanço
de massa e energia, termodinâmica química, mecânica dos fluidos, reologia não-newtoniana,
tubulações industriais, perda de carga, transferência de calor, separação por destilação,
conversão de reagentes e composição de misturas (fração molar/mássica)."""

from .absorcao_stripping import (
    estagios_necessarios_absorcao,
    fator_absorcao,
    fator_esgotamento,
    fracao_nao_absorvida,
    fracao_nao_esgotada,
)
from .adsorcao_troca_ionica import (
    isoterma_freundlich,
    isoterma_langmuir,
    tempo_ruptura_estequiometrico,
)
from .balanco_energia import (
    balanco_energia_escoamento,
    energia_cinetica_especifica,
    energia_potencial_especifica,
    residuo_balanco_energia_global,
)
from .balanco_carbono import emissao_co2_combustao, intensidade_carbono
from .balanco_massa import divisor, misturador, residuo_balanco_massa_global, vazao_desconhecida
from .captura_carbono_ccs import eficiencia_captura, emissao_evitada
from .centrifugacao import forca_g_centrifuga, velocidade_sedimentacao_centrifuga
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
from .doe_fatorial import efeito_principal, numero_ensaios_fatorial
from .confiabilidade_ram import confiabilidade_exponencial, disponibilidade, mtbf, mttr, taxa_falha
from .conversao import (
    grau_avanco,
    mols_a_partir_avanco,
    quantidade_final_a_partir_conversao,
    reagente_limitante,
    rendimento_a_partir_de_mols,
    rendimento_global,
    seletividade,
)
from .controle_pid import parametros_isa_para_paralelo, saida_pid_paralelo
from .conversao import conversao as conversao_reagente
from .cristalizacao import (
    crescimento_cristal_lei_delta_L,
    rendimento_cristalizacao,
    supersaturacao_relativa,
)
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
from .evaporacao import concentracao_final_evaporador, economia_vapor, vapor_gerado_evaporador
from .extracao_liquido_liquido import (
    coeficiente_distribuicao,
    estagios_necessarios_extracao,
    fator_extracao,
    fracao_nao_extraida,
    massa_extraida_estagio_unico,
)
from .fluidizacao import (
    numero_arquimedes,
    queda_pressao_leito_fluidizado,
    velocidade_minima_fluidizacao,
)
from .filtragem import taxa_filtracao, tempo_filtracao_pressao_constante
from .geracao_vapor import eficiencia_caldeira, eficiencia_global_cogeracao, heat_rate_cogeracao
from .eficiencia_energetica import consumo_especifico_energia
from .fmea_rpn import numero_prioridade_risco
from .fta_arvore_falhas import probabilidade_porta_e, probabilidade_porta_ou
from .fracao_molar import (
    fracao_massica_a_partir_molar,
    fracao_molar_a_partir_massica,
    massa_molar_media,
    pressao_parcial,
)
from .integracao_processos_pinch import tabela_problema_pinch
from .hidrodinamica_colunas import (
    parametro_fluxo_fair,
    velocidade_inundacao_souders_brown,
)
from .lixiviacao import concentracao_lixiviado, rendimento_lixiviacao_estagio_ideal
from .metricas_hidricas import intensidade_hidrica, taxa_reuso_agua
from .mecanica_fluidos import (
    numero_reynolds_particula,
    potencia_eixo_bomba,
    potencia_hidraulica_bomba,
    trabalho_bomba_necessario,
    velocidade_terminal_stokes,
)
from .membranas import (
    coeficiente_rejeicao,
    fluxo_permeado,
    seletividade_ideal,
)
from .mistura_agitacao import numero_froude_agitacao, numero_reynolds_agitacao, potencia_agitador
from .moagem import energia_lei_bond, energia_lei_kick, energia_lei_rittinger
from .peneiramento import eficiencia_peneiramento
from .pirolise_gaseificacao import eficiencia_gas_frio
from .psicrometria import (
    approach_torre_resfriamento,
    range_torre_resfriamento,
    razao_umidade,
    umidade_relativa,
)
from .refrigeracao import cop_carnot_bomba_calor, cop_carnot_refrigeracao, cop_refrigeracao
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
from .scale_up import (
    escalonamento_lei_potencia,
    velocidade_escala_froude_constante,
    velocidade_escala_ponta_pa_constante,
    velocidade_escala_potencia_por_volume_constante,
    velocidade_escala_reynolds_constante,
)
from .quimica_verde import economia_atomica
from .secagem import tempo_secagem_taxa_constante, tempo_secagem_taxa_decrescente, tempo_secagem_total
from .seguranca_instrumentada_sil import nivel_sil_a_partir_de_pfd, pfd_media_1oo1
from .sedimentacao import fluxo_massico_solidos, velocidade_sedimentacao_dificultada
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
from .valvulas_controle import (
    caracteristica_igual_percentagem,
    caracteristica_linear,
    cv_necessario,
    vazao_valvula_controle,
)
from .tratamento_agua_caldeira import ciclos_concentracao, vazao_purga
from .tratamento_efluentes import carga_poluente, eficiencia_remocao
from .transferencia_massa import (
    altura_unidade_transferencia,
    fluxo_convectivo_massa,
    fluxo_difusivo_fick,
    forca_motriz_media_log,
    fracao_nao_recuperada_kremser,
    numero_estagios_kremser,
    numero_unidades_transferencia,
)

__all__ = [
    # tratamento_efluentes
    "carga_poluente",
    "eficiencia_remocao",
    # balanco_carbono
    "emissao_co2_combustao",
    "intensidade_carbono",
    # eficiencia_energetica
    "consumo_especifico_energia",
    # integracao_processos_pinch
    "tabela_problema_pinch",
    # quimica_verde
    "economia_atomica",
    # captura_carbono_ccs
    "eficiencia_captura",
    "emissao_evitada",
    # metricas_hidricas
    "intensidade_hidrica",
    "taxa_reuso_agua",
    # pirolise_gaseificacao
    "eficiencia_gas_frio",
    # confiabilidade_ram
    "confiabilidade_exponencial",
    "disponibilidade",
    "mtbf",
    "mttr",
    "taxa_falha",
    # seguranca_instrumentada_sil
    "nivel_sil_a_partir_de_pfd",
    "pfd_media_1oo1",
    # fmea_rpn
    "numero_prioridade_risco",
    # fta_arvore_falhas
    "probabilidade_porta_e",
    "probabilidade_porta_ou",
    # geracao_vapor
    "eficiencia_caldeira",
    "eficiencia_global_cogeracao",
    "heat_rate_cogeracao",
    # refrigeracao
    "cop_carnot_bomba_calor",
    "cop_carnot_refrigeracao",
    "cop_refrigeracao",
    # tratamento_agua_caldeira
    "ciclos_concentracao",
    "vazao_purga",
    # psicrometria
    "approach_torre_resfriamento",
    "range_torre_resfriamento",
    "razao_umidade",
    "umidade_relativa",
    # scale_up
    "escalonamento_lei_potencia",
    "velocidade_escala_froude_constante",
    "velocidade_escala_ponta_pa_constante",
    "velocidade_escala_potencia_por_volume_constante",
    "velocidade_escala_reynolds_constante",
    # doe_fatorial
    "efeito_principal",
    "numero_ensaios_fatorial",
    # controle_pid
    "parametros_isa_para_paralelo",
    "saida_pid_paralelo",
    # valvulas_controle
    "caracteristica_igual_percentagem",
    "caracteristica_linear",
    "cv_necessario",
    "vazao_valvula_controle",
    # filtragem
    "taxa_filtracao",
    "tempo_filtracao_pressao_constante",
    # secagem
    "tempo_secagem_taxa_constante",
    "tempo_secagem_taxa_decrescente",
    "tempo_secagem_total",
    # mistura_agitacao
    "numero_froude_agitacao",
    "numero_reynolds_agitacao",
    "potencia_agitador",
    # lixiviacao
    "concentracao_lixiviado",
    "rendimento_lixiviacao_estagio_ideal",
    # evaporacao
    "concentracao_final_evaporador",
    "economia_vapor",
    "vapor_gerado_evaporador",
    # moagem
    "energia_lei_bond",
    "energia_lei_kick",
    "energia_lei_rittinger",
    # peneiramento
    "eficiencia_peneiramento",
    # sedimentacao
    "fluxo_massico_solidos",
    "velocidade_sedimentacao_dificultada",
    # centrifugacao
    "forca_g_centrifuga",
    "velocidade_sedimentacao_centrifuga",
    # transferencia_massa
    "altura_unidade_transferencia",
    "fluxo_convectivo_massa",
    "fluxo_difusivo_fick",
    "forca_motriz_media_log",
    "fracao_nao_recuperada_kremser",
    "numero_estagios_kremser",
    "numero_unidades_transferencia",
    # absorcao_stripping
    "estagios_necessarios_absorcao",
    "fator_absorcao",
    "fator_esgotamento",
    "fracao_nao_absorvida",
    "fracao_nao_esgotada",
    # extracao_liquido_liquido
    "coeficiente_distribuicao",
    "estagios_necessarios_extracao",
    "fator_extracao",
    "fracao_nao_extraida",
    "massa_extraida_estagio_unico",
    # adsorcao_troca_ionica
    "isoterma_freundlich",
    "isoterma_langmuir",
    "tempo_ruptura_estequiometrico",
    # cristalizacao
    "crescimento_cristal_lei_delta_L",
    "rendimento_cristalizacao",
    "supersaturacao_relativa",
    # hidrodinamica_colunas
    "parametro_fluxo_fair",
    "velocidade_inundacao_souders_brown",
    # membranas
    "coeficiente_rejeicao",
    "fluxo_permeado",
    "seletividade_ideal",
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
