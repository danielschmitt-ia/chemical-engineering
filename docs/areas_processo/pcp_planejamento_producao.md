# Planejamento e Controle de Produção (PCP)

PCP decide o que produzir, quanto e quando — no nível de dias a meses, a camada mais lenta da
hierarquia de decisão operacional descrita em `automacao_avancada.md` (Área 5): abaixo do PCP,
RTO e MPC decidem como operar; acima dele, decisões estratégicas de capacidade/investimento
(`analise_financeira_projetos.py`) fixam o que é fisicamente possível produzir.

## As perguntas centrais do PCP

- **Sequenciamento de campanhas** (em plantas multiproduto/batelada — ex.: uma planta de química
  fina produzindo vários produtos na mesma linha, `sintese_quimicos_finos.md`): em que ordem
  produzir, minimizando tempo de troca (changeover) e limpeza entre campanhas incompatíveis.
- **Dimensionamento de lote**: lotes maiores reduzem a frequência (e o custo total) de troca de
  campanha, mas aumentam estoque em processo e o risco de um lote inteiro sair fora de
  especificação — o mesmo trade-off que `controle_estatistico_processo.py` (Cp/Cpk) ajuda a
  quantificar: um processo mais capaz suporta lotes maiores com risco de não-conformidade menor.
- **Restrição de gargalo**: o PCP precisa conhecer o gargalo real da planta
  (`debottlenecking.md`) para não planejar uma produção que a capacidade física não suporta.

## Onde a otimização estatística e de confiabilidade entram

Um plano de produção realista incorpora a variabilidade e a confiabilidade reais da planta, não
a capacidade nominal de placa de identificação — `confiabilidade_ram.py` (disponibilidade
esperada) e `analise_variabilidade.py` (variabilidade de rendimento/qualidade) alimentam
diretamente o cálculo de quanta capacidade "efetiva" está de fato disponível para planejar contra,
em vez da capacidade teórica de projeto.

## MRP vs. Teoria das Restrições — duas filosofias de PCP

PCP tradicional (MRP — Material Requirements Planning) trabalha de trás para frente a partir da
demanda, calculando necessidades de matéria-prima e capacidade em cada etapa. A Teoria das
Restrições (TOC, Goldratt) argumenta que só vale a pena sincronizar o plano de produção ao redor
do gargalo real (o mesmo gargalo de `debottlenecking.md`) — produzir mais rápido em qualquer etapa
que não seja o gargalo só aumenta estoque em processo, sem aumentar o throughput da planta como um
todo.
