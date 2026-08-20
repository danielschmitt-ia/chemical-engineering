# Validação de Processos Farmacêuticos

Validação de processo farmacêutico (sob GMP — Boas Práticas de Fabricação) é a evidência
documentada de que um processo, operado dentro dos parâmetros especificados, produz
consistentemente um produto que atende suas especificações de qualidade — um requisito
regulatório (ANVISA, FDA), não uma fórmula de engenharia, mas construído diretamente sobre o
controle estatístico de processo (`controle_estatistico_processo.py`) e a confiabilidade
(`confiabilidade_ram.py`) deste pacote.

## As três etapas do ciclo de vida de validação (guia FDA de 2011, amplamente adotado)

1. **Design do processo (Estágio 1)**: define a estratégia de controle a partir do conhecimento
   de desenvolvimento — tipicamente usando design de experimentos (`doe_fatorial.py`) para
   mapear como os parâmetros de processo afetam os atributos críticos de qualidade (CQAs) do
   produto, estabelecendo o "espaço de projeto" (design space) dentro do qual o processo é
   validado para operar.
2. **Qualificação do processo (Estágio 2)**: confirma que o processo, conforme projetado, é
   capaz de produção reprodutível em escala comercial — tipicamente 3 lotes consecutivos dentro
   de especificação são o critério histórico mínimo (a prática atual, orientada a risco, pode
   exigir mais ou menos conforme a complexidade e o histórico do processo).
3. **Verificação contínua do processo (Estágio 3)**: monitoramento estatístico contínuo em
   produção de rotina — a aplicação direta e permanente de `controle_estatistico_processo.py`
   (cartas de controle, Cp/Cpk) para garantir que o processo permanece no estado validado ao
   longo do tempo, não só nos lotes de qualificação inicial.

## Por que "atributo crítico de qualidade" (CQA) é o conceito central

Um CQA é uma propriedade do produto (pureza, dissolução, uniformidade de conteúdo) cuja
variação fora de um limite aceitável compromete a segurança ou eficácia do medicamento — a
validação de processo existe para garantir, com evidência estatística, que a variabilidade natural
do processo (`analise_variabilidade.py`) mantém cada CQA dentro do seu limite com capacidade
suficiente (Cpk adequado, tipicamente >= 1.33 ou mais rígido conforme a criticidade do atributo) —
não confiar em inspeção 100% do produto final, que nunca detecta com certeza um defeito raro.
