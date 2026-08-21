# Descomissionamento de Instalações

Descomissionamento é o processo inverso do comissionamento: tirar uma planta ou unidade de
operação permanentemente de forma segura, removendo os perigos residuais antes da
desmontagem/demolição ou do abandono do site. Não é um cálculo — é uma sequência de segurança,
mas com uma característica que o distingue de uma parada de manutenção normal: o objetivo final é
deixar o equipamento seguro para alguém que não conhece seu histórico de operação.

## A sequência típica

1. **Esvaziamento e limpeza de processo**: remoção do inventário de processo, lavagem/purga de
   linhas e vasos até níveis seguros de material residual (limites tipicamente definidos por
   análise de atmosfera antes de qualquer trabalho a quente ou entrada em espaço confinado).
2. **Isolamento físico** (não só fechamento de válvulas): bloqueio e etiquetagem (lockout/tagout),
   remoção de spools/inserção de bolsas cegas (blind flanges) em interfaces com sistemas ainda
   operacionais — a diferença central frente a uma parada de manutenção é que o isolamento aqui
   precisa ser permanente e à prova de erro humano futuro, não reversível por uma válvula.
3. **Descontaminação**: remoção de resíduos de processo, catalisadores, incrustação
   (`filtragem.py`/depósitos que os módulos de detecção de falha deste repositório monitoram
   durante a operação normal) que possam representar risco quando o equipamento for aberto,
   cortado ou transportado.
4. **Desmontagem/demolição**: com o inventário de risco já removido, a atividade física em si
   segue práticas de segurança de construção civil/estrutural — já não é mais, estritamente,
   segurança de processo.

## Por que isso é diferente de "só desligar"

Um equipamento que operou com material perigoso carrega risco residual mesmo parado e vazio —
resíduos em zonas mortas, incrustação com material pirofórico (comum em serviços de refino,
oxida ao contato com o ar), ou simplesmente a memória institucional de "como isso realmente
funciona" que se perde quando a equipe de operação muda. O descomissionamento formal existe para
não depender dessa memória: documenta e neutraliza o risco antes que ele se torne conhecimento
tácito perdido.
