# Manuseio de Produtos Perigosos

Manuseio de produtos perigosos cobre a classificação (GHS/sistema de Classificação e Rotulagem
Globalmente Harmonizado), armazenamento (compatibilidade química, segregação), transporte e
resposta a emergência de materiais que representam risco à saúde, segurança ou meio ambiente —
principalmente prática regulatória e procedimental, não cálculo, mas com um ponto de contato
direto com a modelagem deste repositório: a classificação de perigo de um material é justamente
o que justifica o rigor da análise de cenário de pior caso que `reator_digital_twin.
simular_runaway` representa.

## Classificação (GHS)

Cada produto químico é classificado em classes e categorias de perigo (físico — inflamabilidade,
reatividade, explosividade; à saúde — toxicidade aguda/crônica; ambiental) com pictogramas e
frases de risco padronizadas internacionalmente — a Ficha de Dados de Segurança (FDS/SDS) é o
documento que consolida essa classificação por produto.

## Compatibilidade e segregação de armazenamento

Produtos incompatíveis (ex.: oxidantes e combustíveis, ácidos e bases fortes, materiais reativos
com água) precisam de segregação física no armazenamento — tipicamente representada em uma
matriz de compatibilidade química. A saponificação modelada em
`reator_digital_twin.rodar_mpc_com_saponificacao` é um exemplo do tipo de reação indesejada
(neutralização ácido-base, aqui entre AGL e catalisador alcalino) que segregação inadequada pode
provocar em escala — embora nesse caso dentro do próprio processo, não no armazenamento.

## Conexão com a análise de pior caso deste repositório

`simular_runaway` usa deliberadamente um calor de reação de pior caso (`DeltaH_cenario`, tipicamente
5x o nominal) em vez da cinética de operação normal — a mesma lógica por trás de tratar um produto
perigoso pelo seu pior cenário crível de liberação (o "credible worst case" de uma análise de
consequência), não pelo cenário mais provável. É essa mesma lógica de pior-caso-crível que
determina, por exemplo, a distância de segurança de armazenamento (`layout_planta_industrial.md`)
ou o dimensionamento de um sistema de alívio de pressão.
