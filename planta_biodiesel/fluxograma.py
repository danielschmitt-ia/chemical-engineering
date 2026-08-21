"""Fluxograma completo de uma planta de biodiesel: da alimentação de óleo até o biodiesel
(FAME) e a glicerina bruta prontos para venda, encadeando os módulos de `calculos_processo/`
em torno do reator de transesterificação já modelado em `reator_digital_twin/` (mesma base de
`configs/exemplo_biodiesel.yaml`).

Diferente de chamar cada função de `calculos_processo/` isoladamente, este módulo resolve um
único problema de ponta a ponta: cada estágio consome a saída do estágio anterior, e o balanço
de massa fecha exatamente por construção — não são exemplos soltos, é uma planta.

Estágios do fluxograma (cada um com sua função dedicada, testável isoladamente):

1. `simular_reator` — conversão de triglicerídeo em FAME + glicerina (`conversao.py`).
2. `simular_decantacao` — separação gravitacional FAME/glicerina (`balanco_massa.divisor`,
   `mecanica_fluidos.velocidade_terminal_stokes`, `sedimentacao.py`).
3. `simular_lavagem` — remoção de glicerina residual do biodiesel bruto por lavagem com água,
   em cascata contracorrente (`extracao_liquido_liquido.py`, equação de Kremser).
4. `simular_recuperacao_metanol` — recuperação do metanol dissolvido no biodiesel lavado
   (`evaporacao.py`).
5. `simular_integracao_termica` — metas de utilidade quente/fria via análise de pinch
   (`integracao_processos_pinch.py`), usando os próprios balanços de massa/energia dos
   estágios anteriores para definir as correntes.
6. `dimensionar_transferencia` — tubulação e bombeamento da linha reator→decantador
   (`perda_carga.py`, `piping.py`, `mecanica_fluidos.py`).
7. `dimensionar_agitacao` — potência do misturador da etapa de lavagem (`mistura_agitacao.py`).
8. `avaliar_seguranca` — FMEA dos principais modos de falha da planta (`fmea_rpn.py`).
9. `avaliar_financeiro` — VPL, payback e TIR do investimento (`analise_financeira_projetos.py`).
10. `avaliar_sustentabilidade` — intensidade hídrica e comparação de CO2 fóssil com diesel
    equivalente (`metricas_hidricas.py`, `balanco_carbono.py`).
11. `economia_atomica_transesterificacao` — economia atômica da própria reação
    (`quimica_verde.py`).

Todos os parâmetros numéricos além da cinética do reator (já validada em
`reator_digital_twin`) são ILUSTRATIVOS — ordem de grandeza plausível de uma planta real, não
dados de projeto. Ver `ParametrosPlantaBiodiesel` para as suposições explícitas de cada estágio.
"""

import math
from dataclasses import dataclass, field

from calculos_processo.analise_financeira_projetos import (
    payback_simples,
    taxa_interna_retorno,
    valor_presente_liquido,
)
from calculos_processo.balanco_carbono import emissao_co2_combustao
from calculos_processo.balanco_massa import divisor, residuo_balanco_massa_global
from calculos_processo.conversao import mols_a_partir_avanco
from calculos_processo.evaporacao import concentracao_final_evaporador, vapor_gerado_evaporador
from calculos_processo.extracao_liquido_liquido import (
    estagios_necessarios_extracao,
    fator_extracao,
    fracao_nao_extraida,
)
from calculos_processo.fmea_rpn import numero_prioridade_risco
from calculos_processo.integracao_processos_pinch import tabela_problema_pinch
from calculos_processo.mecanica_fluidos import (
    potencia_eixo_bomba,
    potencia_hidraulica_bomba,
    velocidade_terminal_stokes,
)
from calculos_processo.metricas_hidricas import intensidade_hidrica
from calculos_processo.mistura_agitacao import numero_reynolds_agitacao, potencia_agitador
from calculos_processo.perda_carga import perda_carga_total
from calculos_processo.piping import espessura_minima_parede
from calculos_processo.quimica_verde import economia_atomica
from calculos_processo.sedimentacao import velocidade_sedimentacao_dificultada


@dataclass
class ParametrosPlantaBiodiesel:
    """Todas as suposições numéricas do fluxograma, em um só lugar. Os valores padrão descrevem
    uma planta de porte médio consistente com `configs/exemplo_biodiesel.yaml` (mesma vazão de
    alimentação: CA0·F = 66.7 mol/min de triglicerídeo)."""

    # --- Reator (ver configs/exemplo_biodiesel.yaml) ---
    vazao_molar_trigliceridio: float = 66.7       # mol/min (= CA0·F do reator)
    razao_molar_metanol_oleo: float = 6.0         # 2x a estequiométrica (3:1) — prática industrial
    conversao_projeto: float = 0.95               # conversão de operação nominal (regime saudável)
    massa_molar_trigliceridio: float = 876.0      # g/mol, óleo vegetal médio (ex.: soja)
    massa_molar_metanol: float = 32.04
    massa_molar_glicerol: float = 92.09
    # massa_molar_fame NÃO é independente — ver `massa_molar_fame()`: precisa fechar a
    # conservação de massa da própria reação (TG + 3 MeOH -> 3 FAME + Glicerol).

    # --- Decantação gravitacional (separação FAME/glicerina) ---
    fracao_fame_fase_leve: float = 0.99           # FAME que fica na fase biodiesel (não polar)
    fracao_glicerol_fase_pesada: float = 0.95     # glicerina que decanta (o resto é a carga da lavagem)
    fracao_metanol_fase_pesada: float = 0.70      # metanol prefere a fase polar (glicerina)
    diametro_gota_glicerol: float = 200e-6        # m — gota dispersa típica em decantador industrial
    rho_fame: float = 880.0                       # kg/m³
    rho_glicerol: float = 1260.0                  # kg/m³
    mu_fame: float = 4.5e-3                       # Pa·s, biodiesel a ~50°C
    porosidade_dispersao: float = 0.75            # ε de Richardson-Zaki (fase leve contínua)

    # --- Lavagem com água (extração líquido-líquido) ---
    coeficiente_distribuicao_glicerol: float = 20.0   # glicerina é muito mais solúvel em água que em FAME
    razao_massica_agua_lavagem: float = 0.15          # água/biodiesel bruto, prática típica
    remocao_alvo_lavagem: float = 0.95                # meta: >=95% do glicerol residual removido

    # --- Recuperação de metanol (evaporador) ---
    pureza_fame_alvo: float = 0.999               # fração mássica de FAME+TG após evaporação do MeOH

    # --- Integração térmica (pinch) ---
    delta_t_min_pinch: float = 10.0                # °C, aproximação mínima entre correntes
    cp_organicos: float = 2.0                      # kJ/(kg·K), óleo/biodiesel/glicerina
    cp_agua: float = 4.18                          # kJ/(kg·K)
    cp_vapor_metanol: float = 1.4                  # kJ/(kg·K), aproximação sensível (ignora latente)
    temperaturas_correntes: dict = field(default_factory=lambda: {
        # (T_suprimento, T_alvo) em °C
        "produto_reator": (55.0, 30.0),      # precisa resfriar antes da decantação
        "vapor_metanol": (65.0, 30.0),       # precisa condensar antes do reciclo
        "oleo_fresco": (20.0, 50.0),         # pré-aquecimento antes do reator
        "agua_lavagem": (15.0, 40.0),        # aquecimento para melhorar a extração
    })

    # --- Tubulação e bombeamento (linha reator -> decantador) ---
    diametro_linha_transferencia: float = 0.05     # m
    comprimento_linha_transferencia: float = 20.0  # m
    rugosidade_absoluta_tubo: float = 4.5e-5       # m, aço carbono comercial
    k_total_acessorios: float = 4.0                # coeficiente de perdas localizadas (válvulas/curvas)
    pressao_projeto_linha: float = 3e5             # Pa
    tensao_admissivel_material: float = 138e6      # Pa, aço carbono típico
    altura_manometrica_bomba: float = 10.0         # m
    eficiencia_bomba: float = 0.65

    # --- Agitação (misturador da lavagem) ---
    diametro_impelidor: float = 0.3                # m
    rotacao_impelidor: float = 3.0                 # rev/s
    numero_potencia_impelidor: float = 5.0         # Po, turbina padrão em regime turbulento

    # --- Financeiro ---
    preco_oleo_kg: float = 1.00
    preco_metanol_kg: float = 0.45
    preco_biodiesel_kg: float = 1.15
    preco_glicerina_kg: float = 0.35
    custo_fixo_diario: float = 3500.0              # mão de obra, manutenção, utilidades
    dias_operacionais_ano: int = 330
    investimento_inicial: float = 8_000_000.0
    vida_util_anos: int = 15
    taxa_desconto: float = 0.12

    # --- Sustentabilidade ---
    fracao_massica_carbono_diesel: float = 0.87
    razao_energetica_biodiesel_diesel: float = 37.5 / 42.6  # MJ/kg biodiesel sobre MJ/kg diesel


def massa_molar_fame(p: ParametrosPlantaBiodiesel) -> float:
    """Massa molar do FAME (biodiesel), derivada da própria conservação de massa da reação de
    transesterificação (TG + 3 MeOH -> 3 FAME + Glicerol) — em vez de um valor médio
    independente, que deixaria o balanço de massa do fluxograma com um resíduo espúrio:

        M_FAME = (M_TG + 3·M_MeOH - M_glicerol) / 3
    """
    return (p.massa_molar_trigliceridio + 3 * p.massa_molar_metanol - p.massa_molar_glicerol) / 3.0


@dataclass
class ResultadoReator:
    trigliceridio_mol_min: float
    metanol_mol_min: float
    fame_mol_min: float
    glicerol_mol_min: float
    massa_molar_fame: float
    massa_entrada_g_min: float
    massa_saida_g_min: float


def simular_reator(p: ParametrosPlantaBiodiesel) -> ResultadoReator:
    """Estágio 1: composição de saída do reator a uma conversão de projeto, pela extensão de
    reação (`conversao.mols_a_partir_avanco`) — reaproveita a mesma lógica estequiométrica da
    Área 2, agora aplicada a vazões molares (mol/min) em vez de mols de batelada, o que é
    dimensionalmente válido porque a relação é linear em ambos os casos."""
    M_fame = massa_molar_fame(p)
    metanol_alimentado = p.razao_molar_metanol_oleo * p.vazao_molar_trigliceridio
    avanco = p.vazao_molar_trigliceridio * p.conversao_projeto

    tg = mols_a_partir_avanco(p.vazao_molar_trigliceridio, -1.0, avanco)
    metanol = mols_a_partir_avanco(metanol_alimentado, -3.0, avanco)
    fame = mols_a_partir_avanco(0.0, 3.0, avanco)
    glicerol = mols_a_partir_avanco(0.0, 1.0, avanco)

    massa_entrada = (p.vazao_molar_trigliceridio * p.massa_molar_trigliceridio
                      + metanol_alimentado * p.massa_molar_metanol)
    massa_saida = (tg * p.massa_molar_trigliceridio + metanol * p.massa_molar_metanol
                   + fame * M_fame + glicerol * p.massa_molar_glicerol)

    residuo = residuo_balanco_massa_global([massa_entrada], [massa_saida])
    assert abs(residuo) < 1e-6 * massa_entrada, f"Balanço de massa do reator não fechou: resíduo={residuo}"

    return ResultadoReator(tg, metanol, fame, glicerol, M_fame, massa_entrada, massa_saida)


@dataclass
class ResultadoDecantacao:
    fase_leve_mol_min: dict
    fase_pesada_mol_min: dict
    velocidade_stokes_m_s: float
    velocidade_sedimentacao_m_s: float
    area_decantador_m2: float


def simular_decantacao(reator: ResultadoReator, p: ParametrosPlantaBiodiesel) -> ResultadoDecantacao:
    """Estágio 2: separação gravitacional entre a fase biodiesel (leve) e a fase glicerina
    (pesada), por diferença de densidade. Cada componente é dividido entre as duas fases com
    `balanco_massa.divisor`; o dimensionamento da área mínima do decantador usa a velocidade de
    sedimentação da gota de glicerina dispersa na fase FAME contínua — Stokes
    (`mecanica_fluidos.velocidade_terminal_stokes`) corrigida por sedimentação dificultada
    (`sedimentacao.velocidade_sedimentacao_dificultada`) — pela equação clássica de
    dimensionamento de decantador por gravidade: Área = vazão volumétrica / velocidade de
    sedimentação (o tempo de residência precisa exceder o tempo de subida/descida da gota)."""
    fame_split = divisor(reator.fame_mol_min, {"leve": p.fracao_fame_fase_leve, "pesada": 1 - p.fracao_fame_fase_leve})
    gli_split = divisor(reator.glicerol_mol_min, {"pesada": p.fracao_glicerol_fase_pesada, "leve": 1 - p.fracao_glicerol_fase_pesada})
    meoh_split = divisor(reator.metanol_mol_min, {"pesada": p.fracao_metanol_fase_pesada, "leve": 1 - p.fracao_metanol_fase_pesada})
    tg_split = divisor(reator.trigliceridio_mol_min, {"leve": 1.0, "pesada": 0.0})

    fase_leve = {"FAME": fame_split["leve"], "Glicerol": gli_split["leve"], "MeOH": meoh_split["leve"], "TG": tg_split["leve"]}
    fase_pesada = {"FAME": fame_split["pesada"], "Glicerol": gli_split["pesada"], "MeOH": meoh_split["pesada"], "TG": tg_split["pesada"]}

    v_stokes = velocidade_terminal_stokes(p.diametro_gota_glicerol, p.rho_glicerol, p.rho_fame, p.mu_fame)
    v_sedimentacao = velocidade_sedimentacao_dificultada(v_stokes, p.porosidade_dispersao)

    vazao_massica_total_kg_min = reator.massa_saida_g_min / 1000.0
    vazao_volumetrica_m3_s = (vazao_massica_total_kg_min / 1000.0) / 60.0  # aprox. rho~1000 kg/m3
    area_decantador = vazao_volumetrica_m3_s / v_sedimentacao

    return ResultadoDecantacao(fase_leve, fase_pesada, v_stokes, v_sedimentacao, area_decantador)


def massa_kg_min(fase_mol_min: dict, p: ParametrosPlantaBiodiesel) -> float:
    """Converte uma fase (dict de componente -> mol/min) para vazão mássica total (kg/min)."""
    M_fame = massa_molar_fame(p)
    massas_molares = {"FAME": M_fame, "Glicerol": p.massa_molar_glicerol,
                       "MeOH": p.massa_molar_metanol, "TG": p.massa_molar_trigliceridio}
    return sum(fase_mol_min[c] * massas_molares[c] for c in fase_mol_min) / 1000.0


@dataclass
class ResultadoLavagem:
    massa_fase_leve_kg_min: float
    massa_agua_kg_min: float
    fator_extracao: float
    remocao_um_estagio: float
    estagios_para_meta: float
    estagios_recomendados: int


def simular_lavagem(decantacao: ResultadoDecantacao, p: ParametrosPlantaBiodiesel) -> ResultadoLavagem:
    """Estágio 3: lavagem com água do biodiesel bruto (fase leve) para remover a glicerina
    residual que não decantou — modelada como extração líquido-líquido em cascata
    contracorrente (`extracao_liquido_liquido.py`, a mesma equação de Kremser de
    `absorcao_stripping.py`), com a água entrando livre de glicerina. Responde à pergunta de
    projeto real: quantos estágios de lavagem são necessários para atingir a meta de remoção?"""
    massa_leve = massa_kg_min(decantacao.fase_leve_mol_min, p)
    massa_agua = p.razao_massica_agua_lavagem * massa_leve

    E = fator_extracao(p.coeficiente_distribuicao_glicerol, massa_agua, massa_leve)
    remocao_1 = 1.0 - fracao_nao_extraida(p.coeficiente_distribuicao_glicerol, massa_agua, massa_leve, N=1)
    n_necessario = estagios_necessarios_extracao(p.coeficiente_distribuicao_glicerol, massa_agua, massa_leve,
                                                  1.0 - p.remocao_alvo_lavagem)
    n_recomendado = max(1, math.ceil(n_necessario))

    return ResultadoLavagem(massa_leve, massa_agua, E, remocao_1, n_necessario, n_recomendado)


@dataclass
class ResultadoRecuperacaoMetanol:
    alimentacao_kg_min: float
    fracao_fame_alimentacao: float
    vapor_metanol_kg_min: float
    biodiesel_final_kg_min: float
    pureza_final: float


def simular_recuperacao_metanol(decantacao: ResultadoDecantacao, p: ParametrosPlantaBiodiesel) -> ResultadoRecuperacaoMetanol:
    """Estágio 4: recuperação do metanol em excesso ainda dissolvido no biodiesel lavado, por
    evaporação (`evaporacao.py`) — o metanol (Teb ~65°C) é muito mais volátil que os ésteres
    (Teb > 300°C), então o balanço de massa do evaporador (soluto não-volátil = FAME+TG, "solvente"
    volátil = metanol) se aplica diretamente. O vapor recuperado é condensado e reciclado à
    alimentação do reator — ver `simular_integracao_termica`, que usa esse mesmo vapor como uma
    das correntes quentes a resfriar."""
    massa_metanol = decantacao.fase_leve_mol_min["MeOH"] * p.massa_molar_metanol / 1000.0
    massa_fame_tg = (decantacao.fase_leve_mol_min["FAME"] * massa_molar_fame(p)
                      + decantacao.fase_leve_mol_min["TG"] * p.massa_molar_trigliceridio) / 1000.0
    alimentacao = massa_fame_tg + massa_metanol
    fracao_fame = massa_fame_tg / alimentacao

    vapor = vapor_gerado_evaporador(alimentacao, fracao_fame, p.pureza_fame_alvo)
    biodiesel_final = alimentacao - vapor
    pureza_final = concentracao_final_evaporador(alimentacao, fracao_fame, vapor)

    return ResultadoRecuperacaoMetanol(alimentacao, fracao_fame, vapor, biodiesel_final, pureza_final)


def simular_integracao_termica(reator: ResultadoReator, lavagem: ResultadoLavagem,
                                recuperacao: ResultadoRecuperacaoMetanol, p: ParametrosPlantaBiodiesel) -> dict:
    """Estágio 5: metas de utilidade quente/fria mínima da planta pelo Problem Table Algorithm
    (`integracao_processos_pinch.tabela_problema_pinch`). As vazões de capacidade térmica (CP)
    de cada corrente vêm diretamente dos balanços de massa já calculados nos estágios 1-4 — não
    são números soltos: o produto do reator (`reator.massa_saida_g_min`), o vapor de metanol
    recuperado (`recuperacao.vapor_metanol_kg_min`), a alimentação fresca de óleo
    (`p.vazao_molar_trigliceridio`) e a água de lavagem (`lavagem.massa_agua_kg_min`) definem as
    quatro correntes do problema."""
    CP_produto_reator = (reator.massa_saida_g_min / 1000.0 / 60.0) * p.cp_organicos
    CP_vapor_metanol = (recuperacao.vapor_metanol_kg_min / 60.0) * p.cp_vapor_metanol
    # p.vazao_molar_trigliceridio (a ALIMENTAÇÃO), não reator.trigliceridio_mol_min (o residual
    # não-reagido que sai do reator) -- mesma distinção de avaliar_financeiro.
    CP_oleo_fresco = (p.vazao_molar_trigliceridio * p.massa_molar_trigliceridio / 1000.0 / 60.0) * p.cp_organicos
    CP_agua_lavagem = (lavagem.massa_agua_kg_min / 60.0) * p.cp_agua

    t = p.temperaturas_correntes
    correntes_quentes = [
        (*t["produto_reator"], CP_produto_reator),
        (*t["vapor_metanol"], CP_vapor_metanol),
    ]
    correntes_frias = [
        (*t["oleo_fresco"], CP_oleo_fresco),
        (*t["agua_lavagem"], CP_agua_lavagem),
    ]
    return tabela_problema_pinch(correntes_quentes, correntes_frias, p.delta_t_min_pinch)


def dimensionar_transferencia(decantacao: ResultadoDecantacao, p: ParametrosPlantaBiodiesel) -> dict:
    """Estágio 6: dimensionamento da linha de transferência reator→decantador — perda de carga
    (`perda_carga.perda_carga_total`), espessura mínima de parede (`piping.
    espessura_minima_parede`) e potência de bombeamento (`mecanica_fluidos.
    potencia_hidraulica_bomba`/`potencia_eixo_bomba`) — usando a mesma vazão volumétrica total já
    calculada para o decantador no estágio 2."""
    # Mesma vazão volumétrica do estágio 2 (decantacao.area_decantador_m2 = vazão/velocidade,
    # por definição), recuperada aqui multiplicando de volta em vez de passá-la solta à parte.
    vazao_volumetrica_m3_s = decantacao.area_decantador_m2 * decantacao.velocidade_sedimentacao_m_s

    perda = perda_carga_total(vazao_volumetrica_m3_s, p.diametro_linha_transferencia,
                               p.comprimento_linha_transferencia, rho=1000.0, mu=p.mu_fame,
                               rugosidade_absoluta=p.rugosidade_absoluta_tubo, K_total=p.k_total_acessorios)
    espessura = espessura_minima_parede(p.pressao_projeto_linha, p.diametro_linha_transferencia,
                                         p.tensao_admissivel_material)
    pot_hidraulica = potencia_hidraulica_bomba(vazao_volumetrica_m3_s, p.altura_manometrica_bomba, rho=1000.0)
    pot_eixo = potencia_eixo_bomba(pot_hidraulica, p.eficiencia_bomba)

    return {"vazao_volumetrica_m3_s": vazao_volumetrica_m3_s, **perda,
            "espessura_parede_m": espessura, "potencia_hidraulica_W": pot_hidraulica,
            "potencia_eixo_bomba_W": pot_eixo}


def dimensionar_agitacao(p: ParametrosPlantaBiodiesel) -> dict:
    """Estágio 7: potência do misturador do tanque de lavagem (`mistura_agitacao.py`) — o
    tanque onde a água de lavagem é dispersa no biodiesel bruto antes da decantação da etapa 3."""
    Re = numero_reynolds_agitacao(1000.0, p.rotacao_impelidor, p.diametro_impelidor, p.mu_fame)
    potencia = potencia_agitador(p.numero_potencia_impelidor, 1000.0, p.rotacao_impelidor, p.diametro_impelidor)
    return {"reynolds_agitacao": Re, "potencia_W": potencia}


def avaliar_seguranca() -> list[dict]:
    """Estágio 8: FMEA simplificada (`fmea_rpn.numero_prioridade_risco`) dos três modos de falha
    mais relevantes desta planta — cada nota (severidade/ocorrência/detecção, escala 1-10) é uma
    avaliação qualitativa ilustrativa, não uma FMEA formal de equipe. A saponificação já tem
    detecção automatizada por resíduo em `reator_digital_twin.ReatorCSTR.
    rodar_mpc_com_saponificacao`, refletida aqui numa nota de detecção melhor que a do risco de
    metanol (sem instrumentação dedicada modelada neste fluxograma)."""
    return [
        {"modo_falha": "Saponificação (AGL na matéria-prima consome o catalisador)",
         "rpn": numero_prioridade_risco(severidade=7, ocorrencia=5, deteccao=3)},
        {"modo_falha": "Vazamento/incêndio de metanol (inflamável, próximo do ponto de ebulição)",
         "rpn": numero_prioridade_risco(severidade=8, ocorrencia=3, deteccao=4)},
        {"modo_falha": "Arraste de glicerina no decantador (upset de vazão/interface)",
         "rpn": numero_prioridade_risco(severidade=4, ocorrencia=6, deteccao=5)},
    ]


@dataclass
class ResultadoFinanceiro:
    producao_fame_kg_dia: float
    producao_glicerina_kg_dia: float
    receita_dia: float
    custo_materia_prima_dia: float
    lucro_dia: float
    margem: float
    fluxo_caixa_anual: float
    vpl: float
    payback_anos: float
    tir: float | None


def avaliar_financeiro(decantacao: ResultadoDecantacao, recuperacao: ResultadoRecuperacaoMetanol,
                        p: ParametrosPlantaBiodiesel) -> ResultadoFinanceiro:
    """Estágio 9: viabilidade econômica (`analise_financeira_projetos.py`) a partir da produção
    e do consumo de matéria-prima já calculados nos estágios anteriores — incluindo o custo do
    óleo vegetal, que domina o custo de produção de biodiesel na prática (frequentemente 70-85%
    do custo variável) e é o motivo pelo qual a margem de uma planta de biodiesel costuma ser
    apertada mesmo com processo bem operado."""
    producao_fame_dia = recuperacao.biodiesel_final_kg_min * 60 * 24
    producao_gli_dia = decantacao.fase_pesada_mol_min["Glicerol"] * p.massa_molar_glicerol / 1000.0 * 60 * 24
    # Consumo de matéria-prima vem da ALIMENTAÇÃO do reator (p.vazao_molar_trigliceridio e a
    # razão molar de metanol), não do que sobra não-reagido em reator.trigliceridio_mol_min/
    # metanol_mol_min — esses são o residual de SAÍDA, não o consumo.
    consumo_oleo_dia = p.vazao_molar_trigliceridio * p.massa_molar_trigliceridio / 1000.0 * 60 * 24
    metanol_alimentado_mol_min = p.razao_molar_metanol_oleo * p.vazao_molar_trigliceridio
    consumo_metanol_dia = metanol_alimentado_mol_min * p.massa_molar_metanol / 1000.0 * 60 * 24

    receita = producao_fame_dia * p.preco_biodiesel_kg + producao_gli_dia * p.preco_glicerina_kg
    custo_materia_prima = consumo_oleo_dia * p.preco_oleo_kg + consumo_metanol_dia * p.preco_metanol_kg
    lucro_dia = receita - custo_materia_prima - p.custo_fixo_diario
    margem = lucro_dia / receita if receita else 0.0

    fluxo_anual = lucro_dia * p.dias_operacionais_ano
    fluxos = [-p.investimento_inicial] + [fluxo_anual] * p.vida_util_anos
    vpl = valor_presente_liquido(fluxos, p.taxa_desconto)
    payback = payback_simples(p.investimento_inicial, fluxo_anual)
    try:
        tir = taxa_interna_retorno(fluxos)
    except ValueError:
        tir = None

    return ResultadoFinanceiro(producao_fame_dia, producao_gli_dia, receita, custo_materia_prima,
                                lucro_dia, margem, fluxo_anual, vpl, payback, tir)


def avaliar_sustentabilidade(financeiro: ResultadoFinanceiro, lavagem: ResultadoLavagem,
                              p: ParametrosPlantaBiodiesel) -> dict:
    """Estágio 10: intensidade hídrica da lavagem (`metricas_hidricas.py`) e comparação de CO2
    fóssil com o diesel equivalente que o biodiesel substitui (`balanco_carbono.py`). O CO2
    liberado na queima do próprio biodiesel é biogênico (o carbono veio da atmosfera via a
    plantação de origem, não de um reservatório fóssil) e por convenção de contabilidade de GEE
    (GHG Protocol) não entra nesta comparação — o benefício de sustentabilidade do biodiesel vem
    de deslocar a queima de diesel fóssil, não de "não emitir CO2 nenhum"."""
    massa_diesel_equivalente_dia = financeiro.producao_fame_kg_dia * p.razao_energetica_biodiesel_diesel
    co2_fossil_evitado_dia = emissao_co2_combustao(massa_diesel_equivalente_dia, p.fracao_massica_carbono_diesel)

    massa_agua_dia_m3 = lavagem.massa_agua_kg_min * 60 * 24 / 1000.0
    intens_hidrica = intensidade_hidrica(massa_agua_dia_m3, financeiro.producao_fame_kg_dia / 1000.0)

    return {"co2_fossil_evitado_kg_dia": co2_fossil_evitado_dia,
            "intensidade_hidrica_m3_por_t": intens_hidrica}


def economia_atomica_transesterificacao(p: ParametrosPlantaBiodiesel) -> float:
    """Estágio 11: economia atômica (`quimica_verde.economia_atomica`) da reação de
    transesterificação em si — tipicamente alta (~90%) porque praticamente todo átomo dos
    reagentes termina no biodiesel ou na glicerina (subproduto vendável), não em um coproduto
    descartado, ao contrário de muitas outras rotas de síntese orgânica."""
    M_fame = massa_molar_fame(p)
    return economia_atomica(M_fame, 3.0, [p.massa_molar_trigliceridio, p.massa_molar_metanol], [1.0, 3.0])


@dataclass
class ResultadoPlantaBiodiesel:
    reator: ResultadoReator
    decantacao: ResultadoDecantacao
    lavagem: ResultadoLavagem
    recuperacao_metanol: ResultadoRecuperacaoMetanol
    pinch: dict
    transferencia: dict
    agitacao: dict
    seguranca: list
    financeiro: ResultadoFinanceiro
    sustentabilidade: dict
    economia_atomica: float


def simular_planta(p: ParametrosPlantaBiodiesel | None = None) -> ResultadoPlantaBiodiesel:
    """Roda o fluxograma completo, estágio por estágio, cada um alimentado pela saída do
    anterior — o ponto de entrada usado por `demo_planta_biodiesel.py`."""
    p = p or ParametrosPlantaBiodiesel()

    reator = simular_reator(p)
    decantacao = simular_decantacao(reator, p)
    lavagem = simular_lavagem(decantacao, p)
    recuperacao = simular_recuperacao_metanol(decantacao, p)
    pinch = simular_integracao_termica(reator, lavagem, recuperacao, p)
    transferencia = dimensionar_transferencia(decantacao, p)
    agitacao = dimensionar_agitacao(p)
    seguranca = avaliar_seguranca()
    financeiro = avaliar_financeiro(decantacao, recuperacao, p)
    sustentabilidade = avaliar_sustentabilidade(financeiro, lavagem, p)
    ae = economia_atomica_transesterificacao(p)

    return ResultadoPlantaBiodiesel(reator, decantacao, lavagem, recuperacao, pinch, transferencia,
                                     agitacao, seguranca, financeiro, sustentabilidade, ae)
