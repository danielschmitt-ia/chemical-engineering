# Destilação Reativa

Combina reação química e destilação no mesmo equipamento: a mistura reage enquanto os produtos
mais voláteis (ou menos voláteis) são continuamente removidos da zona de reação por
vaporização/condensação. Não é tratada como módulo de código isolado em `calculos_processo/`
porque o cálculo real acopla dois fenômenos simultaneamente (equilíbrio líquido-vapor estágio a
estágio, como em `destilacao.py`, e conversão limitada por equilíbrio químico, como em
`termodinamica.constante_equilibrio` e `conversao.py`) — um sistema de equações não-lineares
resolvido estágio a estágio, tipicamente com software de simulação de processos (Aspen Plus
RADFRAC, gPROMS), não uma fórmula fechada.

## Por que funciona

Para uma reação reversível limitada por equilíbrio (ex.: esterificação, produção de MTBE/TAME),
a conversão de equilíbrio em um reator convencional é limitada pela constante de equilíbrio K nas
condições de operação — ver `calculos_processo.termodinamica.constante_equilibrio`. Remover um
produto da zona de reação assim que ele se forma desloca o equilíbrio continuamente na direção
dos produtos (princípio de Le Chatelier), permitindo conversões por passe muito acima do
equilíbrio "estático" de um reator batelada ou CSTR — às vezes eliminando a necessidade de excesso
de reagente ou de reciclo para atingir a conversão-alvo.

## Quando se aplica bem

- Reação e separação ocorrem na mesma faixa de temperatura/pressão (senão a coluna precisa operar
  fora da condição ótima para um dos dois fenômenos).
- Ao menos um produto tem volatilidade suficientemente diferente dos reagentes para ser removido
  seletivamente estágio a estágio.
- Reações equilibradas (esterificação, eterificação, hidrólise) se beneficiam mais do que reações
  irreversíveis rápidas, onde a limitação não é o equilíbrio químico.

## Building blocks já disponíveis neste repositório

- `destilacao.py` — equilíbrio líquido-vapor, Fenske/Underwood/Gilliland/McCabe-Thiele para a
  parte puramente de separação (sem reação), útil como primeira aproximação de quantos estágios a
  separação exigiria isoladamente.
- `conversao.py` e `termodinamica.constante_equilibrio` — conversão de equilíbrio químico
  "estático", útil para estimar o ganho potencial de deslocar o equilíbrio antes de partir para
  uma simulação estágio a estágio completa.
- `cinetica_reatores.py` — cinética de reação, necessária junto com o equilíbrio estágio a
  estágio para saber se a reação é rápida o bastante para se aproximar do equilíbrio dentro do
  tempo de residência em cada prato/estágio (senão a coluna precisa de mais estágios reativos, ou
  de um catalisador mais ativo, para compensar).
