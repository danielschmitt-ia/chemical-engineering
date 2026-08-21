# Licenciamento Ambiental e Regulamentação

Licenciamento ambiental é o processo regulatório de aprovação prévia (no Brasil, tipicamente em
três etapas — Licença Prévia, de Instalação e de Operação) que uma planta industrial precisa
obter antes de ser construída e operada — prática regulatória e jurídica, não cálculo de
engenharia, mas que consome diretamente os resultados quantitativos de vários módulos deste
pacote como evidência técnica.

## As três licenças (modelo brasileiro, CONAMA 237)

1. **Licença Prévia (LP)**: aprova a viabilidade ambiental do projeto na fase de concepção —
   tipicamente exige um Estudo de Impacto Ambiental (EIA/RIMA) para empreendimentos de maior
   porte/potencial poluidor, incluindo a modelagem de dispersão atmosférica de emissões
   (`tratamento_gases_exaustao.md`) e de lançamento de efluentes (`tratamento_efluentes.py`).
2. **Licença de Instalação (LI)**: autoriza a construção, com base no projeto detalhado e nas
   medidas de controle ambiental especificadas na LP.
3. **Licença de Operação (LO)**: autoriza o funcionamento, geralmente após verificação de que os
   sistemas de controle ambiental (tratamento de efluentes, de gases, gestão de resíduos) foram
   implementados e funcionam conforme projetado — precisa ser renovada periodicamente,
   tipicamente condicionada ao cumprimento contínuo dos limites de emissão outorgados.

## Onde os módulos deste pacote entram como evidência técnica

- **Balanço de carbono** (`balanco_carbono.py`) e **eficiência energética**
  (`eficiencia_energetica.py`) — cada vez mais exigidos em processos de licenciamento que incluem
  compromissos de redução de emissões (ex.: como condicionante da licença).
- **Tratamento de efluentes** (`tratamento_efluentes.py`) e **métricas hídricas**
  (`metricas_hidricas.py`) — a base técnica da outorga de uso de água e dos limites de lançamento
  de efluentes.
- **Análise de risco de processo** (`seguranca_processo_industrial.md`, Área 8) — para
  empreendimentos com inventário de material perigoso, o licenciamento tipicamente exige também
  um Estudo de Análise de Risco (EAR), com o mesmo tipo de cenário de pior caso crível que
  `reator_digital_twin.simular_runaway` ilustra.

## Por que isso não é uma fórmula única

Cada jurisdição (no Brasil, cada órgão estadual de meio ambiente, mais o IBAMA para
empreendimentos de impacto federal) tem seus próprios limites de emissão, procedimentos e prazos
— o licenciamento é fundamentalmente um processo administrativo caso a caso, que usa os cálculos
técnicos deste pacote como insumo, não como substituto do processo regulatório em si.
