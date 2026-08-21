# Processos Metalúrgicos e Pirometalurgia

Pirometalurgia extrai e refina metais por processos a alta temperatura — fusão (smelting),
conversão, refino — tipicamente a partir de um minério sulfetado ou óxido. Compartilha a base de
engenharia de reações e transferência de calor deste pacote (balanços de massa e energia,
cinética de reação heterogênea gás-sólido/líquido-sólido), mas com reações e equilíbrios
específicos da metalurgia extrativa que ficam fora do escopo dos módulos genéricos aqui.

## As etapas típicas de uma rota pirometalúrgica

1. **Fusão (smelting)**: o minério concentrado é fundido, tipicamente com um agente redutor
   (coque) e um fundente, para separar o metal (ou uma liga metálica bruta, "matte", no caso de
   sulfetos) da escória (os óxidos indesejados, que flutuam sobre o metal fundido por diferença
   de densidade) — um balanço de massa multi-fase (metal/matte, escória, gás) mais elaborado que
   os balanços bifásicos líquido-vapor deste pacote.
2. **Conversão**: oxidação seletiva do matte para remover enxofre e ferro remanescentes,
   produzindo um metal ainda mais bruto (blister, no caso do cobre).
3. **Refino**: purificação final, frequentemente por eletrólise (a mesma lei de Faraday de
   `eletroquimica.py` — o refino eletrolítico de cobre é um exemplo clássico e direto de
   aplicação industrial dessa lei).

## Por que a termodinâmica de equilíbrio (não cinética) domina o projeto

Diferente de muitos processos deste repositório (onde a cinética de reação e o controle dinâmico
são centrais — o próprio `reator_digital_twin`), processos pirometalúrgicos a alta temperatura
tipicamente se aproximam do equilíbrio termodinâmico rapidamente (temperaturas altas aceleram a
cinética) — o projeto se concentra mais em prever a distribuição de equilíbrio entre as fases
(metal/matte/escória/gás) via diagramas de fase e dados termodinâmicos (a mesma base de
`termodinamica.py`, mas com dados específicos de sistemas metalúrgicos multicomponentes) do que em
modelar a velocidade da reação em si.
