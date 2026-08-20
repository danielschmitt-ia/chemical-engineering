# Segurança de Processo Industrial

Segurança de processo (Process Safety, distinta de segurança ocupacional — que trata de quedas,
cortes, choques elétricos individuais) é a disciplina de prevenir a liberação descontrolada de
energia ou material perigoso — o tipo de evento que mata múltiplas pessoas de uma vez e que motiva
diretamente o `README.md` principal deste repositório (T2 Laboratories, Synthron). Reúne HAZOP,
LOPA, os módulos quantitativos deste pacote (RAM, SIL/PFD, FTA, FMEA — todos em
`calculos_processo/`) e a filosofia de camadas de proteção independentes (IEC 61511) que o SIS do
`reator_digital_twin` ilustra.

## HAZOP (Hazard and Operability Study)

Uma revisão sistemática, nó por nó do fluxograma (P&ID), usando palavras-guia padronizadas (mais,
menos, nenhum, reverso, também, outro que...) aplicadas a cada parâmetro de processo (vazão,
temperatura, pressão, nível, composição) para identificar desvios credíveis e suas causas,
consequências e salvaguardas existentes. Não é redutível a uma fórmula — é um processo estruturado
de brainstorming multidisciplinar, tipicamente conduzido por uma equipe com um facilitador
treinado, sobre o P&ID (`docs/areas_processo/diagramas_pid.md`) detalhado do processo.

## LOPA (Layer of Protection Analysis)

Uma extensão semi-quantitativa do HAZOP: para cada cenário identificado como sério o suficiente,
soma-se a redução de frequência que cada camada de proteção independente (IPL) oferece — cada
IPL, para contar, precisa ser independente da causa iniciadora e das outras camadas, específica
(detecta e responde ao cenário em questão) e auditável. As camadas de proteção deste repositório
ilustram essa lógica diretamente:

1. **BPCS (controle básico)** — o MPC de `reator_digital_twin` com sua restrição de teto de
   temperatura, primeira linha de defesa, mas não conta como IPL independente na LOPA porque
   compartilha o mesmo modelo/sensor que pode estar com defeito na causa iniciadora.
2. **Alarme + intervenção do operador** — não modelado neste repositório, mas tipicamente a
   segunda camada em uma LOPA real.
3. **SIS** — o interlock hard-wired independente (`_avancar_com_sis`), a IPL clássica de LOPA:
   independente do BPCS, dedicada, com sua própria medição.
4. **Proteção mecânica/alívio** — válvula de alívio de pressão, disco de ruptura — não modelada
   aqui, mas tipicamente a última camada antes da contenção secundária.

Cada camada reduz a frequência do cenário por um fator (o PFDavg de
`seguranca_instrumentada_sil.py` é exatamente esse fator para uma camada instrumentada) — a LOPA
soma essas reduções (em log) até que a frequência mitigada fique abaixo do critério de risco
tolerável da empresa/norma aplicável.

## Por que este repositório existe

A combinação restrição-no-MPC + detecção-por-resíduo + SIS-independente deste repositório é uma
implementação de brinquedo, mas estruturalmente fiel, do resultado central de uma LOPA bem feita:
nenhuma camada isolada é suficiente (ver `docs/PROJETO_INDUSTRIAL.md` para o porquê o SIS aqui é
conceitual, não certificado) — a segurança vem da independência entre as camadas, não da
perfeição de nenhuma delas isoladamente.
