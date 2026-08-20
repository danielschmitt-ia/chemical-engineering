# Gestão de Mudanças (MOC — Management of Change)

MOC é o processo formal de revisão e aprovação de qualquer mudança em uma planta — de processo,
equipamento, procedimento ou organizacional — antes de ela ser implementada, para garantir que os
riscos introduzidos pela mudança sejam avaliados com o mesmo rigor do projeto original. Não é um
cálculo, mas é provavelmente a disciplina de segurança de processo mais citada como causa-raiz
indireta de acidentes reais — não porque a mudança em si fosse perigosa, mas porque não passou
pela revisão que teria identificado o risco.

## Por que "mudança temporária" é a categoria mais perigosa

A maioria dos MOCs formais trata mudanças permanentes com o devido rigor. O ponto cego clássico é
a mudança temporária — um jumper elétrico, um bypass de intertravamento, uma linha temporária —
justificada por urgência operacional, que devia ser revertida em dias e nunca foi. O Synthron
(2006, citado no `README.md` principal) é um exemplo do padrão adjacente: um desvio da receita
original (carregar todo o monômero de uma vez, em vez de dosado) sem uma reavaliação formal do
risco de liberação de energia que essa mudança implicava.

## O que um MOC bem estruturado verifica

- **A mudança está dentro do envelope de projeto original?** — ex.: um novo material de
  alimentação, mesmo "parecido" com o original, pode ter cinética diferente (o cenário exato que
  `reator_digital_twin.simular_interlock_seguranca` modela: a planta seguindo uma cinética mais
  severa que a assumida pelo modelo de controle).
- **Alguma camada de proteção existente deixa de ser válida?** — ex.: um SIS dimensionado para um
  ΔHrx nominal pode não ser suficiente se a mudança altera esse valor (ver
  `sis_intertravamento_seguranca.md`).
- **Os documentos vivos foram atualizados?** — P&ID, procedimentos operacionais, treinamento —
  um MOC sem atualização de documentação cria exatamente o descasamento entre "o que está escrito"
  e "como a planta realmente opera" que investigações de acidentes rotineiramente encontram.
- **Data de expiração para mudanças temporárias**, com revisão obrigatória antes de expirar —
  o controle específico contra o padrão "temporário que nunca voltou ao normal".
