# Manutenção Preditiva e Proativa

Manutenção preditiva monitora a condição real do equipamento (vibração, temperatura, resíduo de
processo, análise de óleo) para prever a falha antes que ela ocorra, em vez de trocar
componentes por um calendário fixo (manutenção preventiva) ou esperar a falha acontecer
(manutenção corretiva). Este repositório já implementa o exemplo mais direto desse princípio
aplicado a processo, não a um componente mecânico: a detecção de falha por resíduo de
`reator_digital_twin/modelo.py` (fouling do UA, desativação catalítica por saponificação) —
mesma lógica de "detectar a degradação antes que vire falha", aplicada ao processo em vez de a um
rolamento ou motor.

## Os quatro níveis de estratégia de manutenção (do mais reativo ao mais proativo)

1. **Corretiva**: conserta depois que quebra. Mais barata por evento, mais cara no total (parada
   não planejada, dano consequente, risco de segurança se a falha for perigosa).
2. **Preventiva**: troca/revisa por calendário ou uso acumulado, independente da condição real —
   reduz falhas inesperadas, mas desperdiça vida útil de componentes que ainda estavam bons.
3. **Preditiva**: monitora a condição real e age quando há evidência de degradação — o
   `reator_digital_twin` ilustra essa lógica: a EWMA do resíduo entre temperatura medida e
   prevista sinaliza o fouling do UA *antes* que ele se torne um evento de segurança, mesmo
   enquanto o MPC ainda consegue mascarar o sintoma mantendo o setpoint.
4. **Proativa** (ou baseada em confiabilidade — RCM/MCC, ver `manutencao_centrada_confiabilidade_
   mcc.md`): vai além de detectar degradação — ataca a causa-raiz para eliminar o modo de falha
   por completo (ex.: melhorar a filtração da água de resfriamento para reduzir a taxa de fouling
   em vez de só monitorar e reagir a ela).

## Por que a detecção por resíduo (não só monitoramento de vibração) importa em processos químicos

A manutenção preditiva "clássica" (vibração, análise de óleo) monitora saúde mecânica de
equipamento rotativo. Processos químicos têm um modo de degradação adicional que não tem
assinatura mecânica: a *deriva do próprio processo* frente ao modelo que o controla — exatamente
o que os dois cenários de falha do `reator_digital_twin` (fouling, saponificação) demonstram. Um
sensor de vibração não detectaria nenhum dos dois; só a comparação entre o comportamento medido e
o previsto pelo modelo nominal revela a degradação.
