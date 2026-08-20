# Utilidades e Sistemas Auxiliares

"Utilidades" é o termo do setor para a infraestrutura que serve o processo principal sem fazer
parte dele diretamente — vapor (`geracao_vapor.py`), água de resfriamento e torres
(`psicrometria.py`), refrigeração (`refrigeracao.py`), água tratada e de caldeira
(`tratamento_agua_caldeira.py`), ar comprimido, nitrogênio/gases inertes, e a distribuição
elétrica da planta. Não é um cálculo isolado — é a integração desses sistemas (cada um já com seu
módulo específico) mais os que ficam fora do escopo de fórmula fechada abaixo.

## Sistemas de utilidades não cobertos por um módulo dedicado

- **Ar comprimido de instrumentação e de processo**: dimensionamento de compressores e secadores
  de ar — a mesma lógica de `refrigeracao.py` (COP, ciclo termodinâmico) se aplica ao ciclo de
  refrigeração de um secador de ar por refrigeração, mas o dimensionamento do compressor de ar em
  si (deslocamento positivo vs. centrífugo, múltiplos estágios) é mais uma escolha de equipamento
  que um cálculo de processo.
- **Geração e distribuição de nitrogênio/gases inertes**: usados para inertização (purga de
  atmosfera explosiva antes de manutenção, blanketing de tanques de inflamáveis) — conecta
  diretamente com a análise de segurança de processo (Área 8).
- **Distribuição elétrica da planta**: fora do escopo de engenharia de processos deste
  repositório — é engenharia elétrica (dimensionamento de transformadores, coordenação de
  proteção, estudo de curto-circuito).

## Por que a confiabilidade das utilidades importa desproporcionalmente

Uma falha de utilidade (perda de energia elétrica, perda de água de resfriamento, perda de ar de
instrumentação) tipicamente afeta *toda* a planta simultaneamente, não uma única unidade — é
exatamente o tipo de cenário credível que uma análise de segurança de processo (HAZOP/LOPA)
precisa considerar explicitamente, porque tende a colocar múltiplos sistemas de proteção em
demanda ao mesmo tempo (ex.: perda de água de resfriamento tira a capacidade de resfriamento
justo quando o SIS de `reator_digital_twin` mais precisaria dela para conter um cenário de
runaway).
