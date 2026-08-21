# Biocombustíveis e Biorrefinarias

Este repositório já trata biodiesel como uma das três aplicações industriais demonstradas do
gêmeo digital (`configs/exemplo_biodiesel.yaml`, `demo_saponificacao.py`) — a transesterificação
alcalina (triglicerídeo + metanol → éster + glicerol), seu modo de falha real mais comum
(saponificação: ácidos graxos livres neutralizando o catalisador, modelado em
`reator_digital_twin.rodar_mpc_com_saponificacao`), e por que o Economic MPC e o soft sensor
importam mais que a análise de fuga térmica nesse processo (reação termicamente branda) — ver a
seção "Aplicações Industriais" do `README.md` principal.

O reator é só a primeira etapa: `planta_biodiesel/fluxograma.py` estende essa mesma matéria-prima
e conversão até o produto acabado — decantação gravitacional, lavagem, recuperação de metanol,
integração térmica, dimensionamento de utilidades, segurança (FMEA) e viabilidade econômica —
ver a seção "Fluxograma Completo" do `README.md` principal e `demo_planta_biodiesel.py`.

## O conceito de biorrefinaria

Uma biorrefinaria processa biomassa em múltiplos produtos simultaneamente (combustíveis,
produtos químicos, energia, ração animal), análogo a uma refinaria de petróleo convencional —
maximizando o valor extraído da matéria-prima em vez de produzir um único produto. Rotas comuns:

- **Rota bioquímica** (fermentação): açúcares → etanol (a rota do etanol de cana-de-açúcar/milho),
  usando cinética de bioprocesso (Monod, `bioreatores.py`) em vez de cinética química clássica.
- **Rota química** (transesterificação): óleos/gorduras → biodiesel — a rota já modelada neste
  repositório.
- **Rota termoquímica** (pirólise/gaseificação, `pirolise_gaseificacao.py`): biomassa
  lignocelulósica (resíduo agrícola, madeira) → bio-óleo ou gás de síntese, útil justamente para
  matérias-primas que não se prestam às rotas bioquímica/química (celulose e lignina, não açúcar
  ou óleo).

## Por que a matéria-prima determina a rota (e o modo de falha)

Diferente de uma planta petroquímica com alimentação de composição relativamente estável, uma
biorrefinaria lida com matéria-prima biológica de composição variável (índice de acidez do óleo,
teor de umidade da biomassa, composição do caldo de fermentação) — exatamente a fonte da falha
por saponificação modelada neste repositório: a qualidade da matéria-prima (fração de AGL) piora
ao longo do tempo de um jeito que um processo com alimentação sintética pura normalmente não
enfrentaria, motivando o tipo de detecção de falha por resíduo que o `reator_digital_twin`
implementa.
