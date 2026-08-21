# Engenharia de Superfícies

Engenharia de superfícies modifica a camada superficial de um material (revestimentos, tratamento
térmico superficial, tratamento químico) para melhorar propriedades específicas — resistência à
corrosão, resistência ao desgaste, redução de atrito — sem alterar as propriedades do substrato
como um todo. Conecta diretamente com `engenharia_corrosao.py`: um revestimento de proteção contra
corrosão é frequentemente a alternativa de menor custo frente a construir o equipamento inteiro em
uma liga mais resistente.

## Técnicas comuns em equipamento de processo

- **Revestimentos metálicos**: galvanização (zinco, proteção catódica de sacrifício — o zinco
  corrói preferencialmente ao aço, protegendo-o mesmo onde o revestimento tem falhas pontuais),
  cladeamento (uma camada de liga resistente, ex.: aço inoxidável, metalurgicamente ligada a um
  substrato de aço carbono mais barato — comum em vasos de pressão que só precisam de resistência
  à corrosão na superfície molhada pelo processo).
- **Revestimentos não-metálicos**: pintura industrial (a barreira mais comum e mais barata,
  mas a menos duradoura das opções aqui), revestimentos poliméricos/epóxi (para serviços químicos
  específicos), revestimentos cerâmicos (resistência a abrasão/altíssima temperatura).
- **Tratamento térmico superficial**: cementação, nitretação — endurecem a superfície de uma
  peça metálica (relevante para desgaste em equipamento rotativo/partes móveis) sem fragilizar o
  núcleo, que mantém tenacidade.

## Por que a escolha é sempre um trade-off custo-vida útil

Um revestimento de proteção nunca é permanente — cada técnica tem uma vida útil esperada e um
custo de reaplicação/manutenção (conectando com `manutencao_centrada_confiabilidade_mcc.md`,
Área 8) — a decisão de qual técnica usar (e não simplesmente "usar a liga resistente inteira")
é uma otimização entre custo de capital inicial, custo de manutenção recorrente ao longo da vida
do equipamento, e o risco de falha entre intervenções — a mesma lógica de `gestao_ativos_
industriais.md` (Área 8) aplicada à escolha de revestimento em vez de material de construção.
