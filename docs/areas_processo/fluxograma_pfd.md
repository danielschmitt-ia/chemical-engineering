# Fluxogramas de Processo (PFD)

Um PFD (Process Flow Diagram) mostra o fluxo principal do processo — equipamentos principais,
correntes entre eles, e os dados de processo essenciais (vazão, temperatura, pressão, composição
em uma tabela de correntes) — em um nível de detalhe conceitual, sem a instrumentação e as
válvulas manuais de um P&ID (`diagramas_pid.md`). É uma convenção de representação, não um
cálculo, mas a tabela de correntes que o acompanha é diretamente o resultado dos balanços de
massa e energia (`balanco_massa.py`, `balanco_energia.py`) deste pacote.

## O que um PFD tipicamente inclui

- **Equipamentos principais** representados por símbolos simplificados (sem detalhe de bocais,
  suportes, instrumentação).
- **Correntes principais**, numeradas, ligando os equipamentos.
- **Tabela de balanço de massa e energia** — para cada corrente numerada: vazão, composição,
  temperatura, pressão, fase. Essa tabela é exatamente o tipo de resultado que `balanco_massa.
  misturador`/`divisor` e `balanco_energia.balanco_energia_escoamento` produzem para cada unidade
  do fluxograma.
- **Malhas de controle principais** (só as estratégicas para entender o processo — ex.: controle
  de nível de um vaso — sem o detalhe completo de instrumentação de um P&ID).

## PFD vs. P&ID — quando usar cada um

| | PFD | P&ID |
|---|---|---|
| Fase do projeto | Conceitual/básico | Detalhamento/executivo |
| Público | Gerência, revisão de processo, licenciamento ambiental | Operação, manutenção, comissionamento |
| Nível de detalhe | Equipamentos principais + balanço de massa/energia | Toda válvula, instrumento, linha, intertravamento |
| Atualização | Estável após o projeto básico | Vivo — atualizado a cada modificação de planta (ver `docs/areas_processo/gestao_mudancas_moc.md`, Área 8) |

Um PFD costuma ser o primeiro documento gerado a partir de uma simulação de processo em regime
permanente (ver `modelagem_simulacao_processos.md`) — a tabela de correntes vem diretamente da
convergência do balanço de massa e energia do fluxograma simulado.
