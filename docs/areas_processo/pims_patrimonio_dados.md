# Patrimônio de Dados Industriais (PIMS)

Um PIMS (Process Information Management System — ex.: OSIsoft PI, AVEVA Historian, Aspen IP.21) é
a infraestrutura que coleta, comprime, armazena e disponibiliza os dados de processo em série
temporal de uma planta (temperaturas, pressões, vazões, posições de válvula — tipicamente
centenas de milhares de tags, amostrados de segundos a minutos, retidos por anos). Não é tratado
como cálculo porque é fundamentalmente arquitetura de dados e infraestrutura de TI/TO, não uma
fórmula de engenharia — mas é o alicerce sobre o qual quase todo o resto deste repositório se
apoia em uma planta real: soft sensors, detecção de falha por resíduo, e RTO (`docs/areas_processo/
automacao_avancada.md`) todos dependem de um histórico de dados de processo confiável e acessível.

## Por que compressão importa

Um PIMS tipicamente usa compressão com perda controlada (ex.: o algoritmo *swinging door*/
exception-deviation) para armazenar só os pontos que mudam significativamente, em vez de cada
amostra bruta — reduzindo o volume de armazenamento em ordens de grandeza sem perder a forma do
sinal dentro de uma tolerância configurada por tag. Configurar essa tolerância errado (grande
demais) é uma causa comum e sutil de um soft sensor ou detector de falha por resíduo
(`reator_digital_twin/modelo.py`) treinado ou calibrado com dados históricos que não refletem a
dinâmica real do processo.

## Onde isso se conecta com o resto do repositório

- **Soft sensors** (o ensemble de redes neurais do `reator_digital_twin`) são tipicamente
  treinados com dados históricos extraídos de um PIMS real, não gerados por simulação, em uma
  planta de produção.
- **Detecção de falha por resíduo** (fouling, saponificação) depende de ter o histórico de UA
  nominal e da variável monitorada disponível e com granularidade temporal suficiente para
  calcular a EWMA do resíduo sem ruído de amostragem excessivo.
- **A camada de integração OPC-UA** (`reator_digital_twin/integracao/`) deste repositório é o tipo
  de fonte que um PIMS real consumiria continuamente em produção — o servidor/gateway simulados
  aqui representam esse papel.
