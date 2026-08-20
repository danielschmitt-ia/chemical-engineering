# Síntese de Produtos Químicos Finos

Produção de compostos orgânicos de alto valor agregado e baixo volume (intermediários
farmacêuticos, agroquímicos, aromas e fragrâncias, aditivos especiais) — tipicamente em reatores
batelada ou semibatelada multipropósito, com rotas de síntese multi-etapas. Não é um cálculo
fechado como os demais itens desta área: é uma prática de engenharia que combina cinética de
reação (`cinetica_reatores.py`), balanços de massa e conversão (`balanco_massa.py`,
`conversao.py`) e considerações específicas do contexto de baixo volume/alto valor agregado
listadas abaixo.

## O que muda frente a um processo contínuo de commodity

- **Rendimento importa mais que utilização de capital**: com poucas toneladas/ano e matéria-prima
  cara, um ponto percentual de rendimento (`conversao.rendimento_global`,
  `conversao.rendimento_a_partir_de_mols`) frequentemente vale mais do que a produtividade
  volumétrica do reator — o oposto da lógica de otimização de uma planta de commodities.
  Purificação (múltiplos passes de destilação, recristalização) que sacrifica rendimento por
  pureza costuma ser aceita, dado o alto valor do produto por kg.
- **Rotas multi-etapas**: cada etapa tem sua própria conversão e seletividade
  (`conversao.grau_avanco`, `conversao.seletividade`); o rendimento global da rota é o produto dos
  rendimentos de cada etapa — um argumento forte a favor de minimizar o número de etapas em
  projeto de rota (síntese convergente vs. linear).
- **Scale-up não trivial**: um reator batelada multipropósito de planta piloto para produção
  raramente escala apenas linearmente — tempo de mistura, transferência de calor (razão
  área/volume cai com a escala) e tempo de adição de reagente mudam o perfil de concentração
  local e podem alterar seletividade entre rotas competitivas. Ver a área "Scale-up de Processos"
  (`docs/areas_processo/` desta mesma série) para os grupos adimensionais usados nesse tipo de
  extrapolação.
- **Regulamentação e qualidade**: para intermediários farmacêuticos, o processo frequentemente
  precisa seguir Boas Práticas de Fabricação (GMP) e ser validado (ver
  `docs/areas_processo/validacao_farmaceutica.md` quando essa área for tratada) — impurezas
  genotóxicas e polimorfismo de cristalização (ver `cristalizacao.py` quando essa área for
  tratada) são preocupações que não existem, ou são muito menos críticas, em química de
  commodities.
