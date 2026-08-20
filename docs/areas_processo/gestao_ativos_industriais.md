# Gestão de Ativos Industriais

Gestão de ativos (Asset Management, formalizada pela ISO 55000) é a disciplina de decidir onde
investir capital de manutenção/substituição para maximizar o valor extraído do parque de
equipamentos ao longo do seu ciclo de vida — a camada de decisão que usa como insumo as métricas
de `confiabilidade_ram.py` (MTBF, disponibilidade) e a priorização de `manutencao_centrada_
confiabilidade_mcc.md`, mas no nível de portfólio (qual ativo, entre centenas, priorizar) em vez
de equipamento individual.

## A pergunta central: criticidade vs. condição

Um programa de gestão de ativos maduro cruza duas dimensões independentes para cada equipamento:

- **Criticidade**: quão grave seria a consequência de uma falha (segurança, produção, ambiental,
  reputacional) — a mesma pergunta central de uma FMEA (`fmea_rpn.py`) ou de uma LOPA
  (`seguranca_processo_industrial.md`), aplicada no nível do ativo.
- **Condição/confiabilidade atual**: quão perto o equipamento está de falhar — informada por
  MTBF/disponibilidade histórica (`confiabilidade_ram.py`) e por dados de monitoramento de
  condição (`manutencao_preditiva_proativa.md`).

Um ativo de alta criticidade e baixa confiabilidade atual é a prioridade óbvia de investimento;
um ativo de baixa criticidade, mesmo com confiabilidade ruim, pode ser deixado para manutenção
corretiva sem grande risco — a mesma lógica de triagem do RCM, aplicada ao orçamento de capital em
vez de à estratégia de manutenção de um único equipamento.

## Por que isso é mais que manutenção

Gestão de ativos também informa decisões de longo prazo que manutenção sozinha não cobre:
substituir vs. reformar (a curva de custo total de propriedade de um equipamento envelhecendo
tipicamente cruza a de um novo em algum ponto), dimensionamento de sobressalentes críticos
(quanto estoque de peças de reposição vale manter para um ativo de alta criticidade e prazo de
entrega longo), e priorização de capital entre unidades/plantas competindo pelo mesmo orçamento —
decisões de portfólio que dependem de dados de confiabilidade agregados, não de um único
equipamento isolado.
