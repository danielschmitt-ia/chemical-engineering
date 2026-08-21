# Logística e Suprimentos Internos

Logística industrial interna cobre o fluxo físico de matéria-prima, produto em processo e produto
acabado dentro de uma planta e sua cadeia de suprimentos imediata — armazenamento, movimentação
(dutovias, tanques, silos, caminhões-tanque), e a interface com o planejamento de produção
(`pcp_planejamento_producao.md`) que decide quando e quanto produzir. Prática de operações, não
cálculo isolado, mas com pontos de contato diretos com os módulos deste pacote.

## Onde este pacote entra

- **Dimensionamento de tubulação/transporte** entre áreas de armazenamento e processo:
  `perda_carga.py` e `transporte_pneumatico_solidos.md` (para sólidos a granel).
- **Dimensionamento de tanques de estocagem intermediária (buffer)**: o volume de buffer entre
  duas etapas de processo com taxas de produção/consumo diferentes é dimensionado por um balanço
  de massa acumulado ao longo do tempo — a mesma lógica de `balanco_massa.residuo_balanco_massa_
  global`, integrada no tempo em vez de avaliada em regime permanente.
- **Gestão de estoque de sobressalentes críticos**: conecta diretamente com
  `gestao_ativos_industriais.md` (Área 8) — o dimensionamento de estoque de peças de reposição
  para um ativo de alta criticidade e prazo de entrega longo é uma decisão logística informada
  por confiabilidade (`confiabilidade_ram.py`).

## Por que buffer entre etapas de processo é uma decisão de risco, não só de espaço

Um buffer de estoque intermediário generoso desacopla etapas de processo com confiabilidades
diferentes (uma falha a montante não para imediatamente a etapa a jusante) — mas cada unidade de
buffer tem custo de capital, espaço e, para materiais reativos/instáveis, risco próprio de
degradação durante a estocagem. O dimensionamento correto pondera a probabilidade e duração
esperada de uma parada a montante (informada pelas métricas de `confiabilidade_ram.py`) contra o
custo de manter aquele buffer — não uma regra fixa de "X horas de estoque" aplicada uniformemente
a toda a planta.
