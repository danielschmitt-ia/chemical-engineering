# Fabricação de Celulose e Papel

A produção de celulose (polpação — separar a fibra de celulose da lignina que a mantém unida na
madeira) e sua conversão em papel combina várias operações unitárias já cobertas por este pacote,
aplicadas a um sistema fibroso específico, mais etapas específicas do setor (branqueamento, a
máquina de papel em si) fora do escopo de fórmula fechada aqui.

## As etapas principais, e onde este pacote se aplica

- **Polpação (kraft, o processo dominante hoje)**: cozimento da madeira com uma solução alcalina
  (hidróxido de sódio + sulfeto de sódio, o "licor branco") sob pressão e temperatura — um reator
  em batelada ou contínuo cuja cinética de deslignificação segue a mesma lógica de cinética de
  reação de `cinetica_reatores.py`, embora com uma reação heterogênea líquido-sólido específica.
- **Recuperação química (ciclo de recuperação kraft)**: o licor negro (subproduto rico em lignina
  dissolvida e produtos químicos de cozimento) é concentrado por evaporação de múltiplo efeito
  (a mesma base de `evaporacao.py`, mas com um licor viscoso e incrustante — um caso extremo do
  tipo de fouling que `reator_digital_twin` modela para o UA de um trocador) e queimado em uma
  caldeira de recuperação, que também gera vapor (`geracao_vapor.py`) e regenera os químicos de
  cozimento — um dos exemplos mais completos de integração de processos (`integracao_processos_
  pinch.py`) na indústria de processo, porque a planta é ao mesmo tempo produtora e consumidora
  intensiva de energia.
- **Branqueamento**: sequência de estágios de oxidação seletiva (historicamente com cloro
  elementar, hoje predominantemente ECF — dióxido de cloro — ou TCF — livre de cloro, por
  pressão ambiental/regulatória) para remover a lignina residual sem degradar a fibra de
  celulose — fora do escopo de fórmula fechada deste pacote.
- **Máquina de papel**: formação da folha por drenagem de uma suspensão diluída de fibras sobre
  uma tela (uma operação de filtração especializada, relacionada a `filtragem.py`, mas em regime
  contínuo de alta velocidade), seguida de prensagem e secagem (`secagem.py`).

## Por que esse setor é intensivo em integração de processos

Uma planta de celulose kraft moderna é tipicamente autossuficiente ou exportadora líquida de
energia (a queima do licor negro na caldeira de recuperação supre a maior parte, às vezes toda, a
demanda de vapor e eletricidade da planta) — o tipo de resultado que uma análise de pinch bem
executada (`integracao_processos_pinch.py`) exatamente busca maximizar, recuperando o máximo de
calor possível entre as correntes do processo antes de recorrer a energia externa.
