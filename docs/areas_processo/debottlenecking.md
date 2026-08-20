# Debottlenecking (Desengarrafamento)

Debottlenecking é o processo sistemático de identificar e remover o(s) equipamento(s) que
limitam a capacidade de produção de uma planta, para aumentar throughput sem construir uma
unidade nova — tipicamente o investimento com melhor retorno disponível para uma planta existente
(a estrutura de capital fixo já está paga; o ganho de capacidade vem de um investimento pontual
no gargalo real). Não é uma fórmula isolada, mas segue uma lógica bem definida que usa vários
módulos deste pacote como ferramentas de diagnóstico.

## A lógica central: só o gargalo importa

Em uma planta com equipamentos em série, aumentar a capacidade de qualquer equipamento que NÃO
seja o gargalo não aumenta o throughput da planta — o gargalo (o equipamento operando mais perto
do seu limite) segue restringindo tudo. A sequência de debottlenecking correta é:

1. **Identificar o gargalo real** — nem sempre óbvio; requer verificar a margem de capacidade de
   cada equipamento na sequência (ex.: perda de carga disponível vs. necessária em
   `perda_carga.py`, área de troca térmica instalada vs. necessária em `transferencia_calor.py`,
   ΔP disponível em uma válvula de controle já quase totalmente aberta em
   `valvulas_controle.py` — sinal clássico de um gargalo de controle).
2. **Remover ou expandir esse gargalo específico** — com a menor intervenção possível (trocar um
   internals de coluna, aumentar o diâmetro de um trecho de tubulação, adicionar área de troca
   térmica) em vez de substituir o equipamento inteiro, quando viável.
3. **Reavaliar**: depois de remover um gargalo, outro equipamento (que tinha folga suficiente
   antes) se torna o novo gargalo — debottlenecking é tipicamente iterativo, não uma correção
   única.

## Por que isso conecta com scale-up/scale-down

Um debottlenecking bem-sucedido frequentemente precisa das mesmas regras de escalonamento de
`scale_up.py` — expandir a capacidade de um único equipamento (ex.: um agitador) exige entender
como as grandezas de processo relevantes (potência, tempo de mistura) escalam com a mudança de
tamanho, para garantir que o desempenho do processo (não só a capacidade nominal) se mantém.
