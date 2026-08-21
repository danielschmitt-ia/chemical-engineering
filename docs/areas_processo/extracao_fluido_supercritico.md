# Extração por Fluido Supercrítico

Extração usando um solvente acima do seu ponto crítico (CO2 supercrítico é o mais comum na
indústria — descafeinação, extração de óleos essenciais, produtos farmacêuticos, por não deixar
resíduo de solvente tóxico) — combina densidade líquida (alto poder de solvatação) com
viscosidade e difusividade de gás (transporte rápido). Não é tratada como módulo de código porque
o parâmetro central de projeto, o poder de solvatação (essencialmente a solubilidade do soluto no
fluido supercrítico em função de pressão e temperatura), não tem uma fórmula fechada confiável de
uso geral — depende de correlações empíricas ajustadas por sistema soluto-solvente (ex.: modelos
de densidade associados a uma equação de estado cúbica, como Peng-Robinson, ou correlações
puramente empíricas tipo Chrastil), tipicamente obtidas experimentalmente ou por regressão de
dados de solubilidade publicados para aquele par específico.

## Por que a região supercrítica importa

Acima do ponto crítico (para CO2: Tc ≈ 31 °C, Pc ≈ 73.8 bar) não existe mais uma fronteira
líquido-vapor distinta — o fluido tem uma única fase cujas propriedades variam continuamente
com pressão e temperatura. O ponto de operação central do projeto é justamente explorar essa
variação contínua: pequenos ajustes de pressão (a temperatura constante) mudam a densidade do
fluido de forma acentuada perto do ponto crítico, e a densidade é o principal fator que controla
o poder de solvatação — o que permite "sintonizar" a seletividade e a capacidade de extração sem
trocar de solvente, e também permite uma separação limpa do soluto simplesmente despressurizando
o CO2 no final (ele volta a ser gás e se desprende do soluto sem deixar resíduo).

## O que costuma ser calculado (fora do escopo deste repositório)

- **Solubilidade do soluto** em função de P e T — via correlação empírica ajustada ao sistema
  específico (ex.: Chrastil) ou via equação de estado cúbica com regras de mistura, tipicamente
  resolvida numericamente, não em forma fechada.
- **Densidade do CO2 supercrítico** em função de P e T — via equação de estado (Span-Wagner para
  alta precisão, ou Peng-Robinson para uma estimativa de engenharia), também não redutível a uma
  fórmula fechada simples de uso geral na faixa supercrítica.
- **Razão solvente/alimentação e número de estágios de equilíbrio** — uma vez que a solubilidade
  (equilíbrio) é conhecida, o dimensionamento do processo de extração em si segue a mesma lógica
  de balanço de massa em estágios de `extracao_liquido_liquido.py` (Kremser), só que com uma fase
  supercrítica no lugar do solvente líquido convencional.
