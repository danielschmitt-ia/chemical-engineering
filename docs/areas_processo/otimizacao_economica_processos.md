# Otimização Econômica de Processos

Não é um módulo separado porque este repositório já implementa o exemplo mais direto de
otimização econômica em tempo real: `reator_digital_twin.rodar_mpc_economico` (Economic MPC) —
substitui o custo de rastreamento de setpoint por um custo econômico direto (receita da conversão
menos custo energético da jaqueta), a cada passo do horizonte de controle, respeitando as mesmas
restrições de segurança do MPC de rastreamento. Ver a seção "💰 Economic MPC" do `README.md`
principal.

## Os dois níveis de otimização econômica de processo

1. **Tempo real (Economic MPC)**: já coberto — otimiza a operação minuto a minuto, dentro do
   espaço de decisão disponível ao controle avançado (setpoints, cargas térmicas).
2. **Nível de projeto/planejamento**: decisões de capital que fixam o espaço de operação
   disponível para o Economic MPC operar depois — dimensionamento de equipamento, seleção de
   tecnologia, avaliadas por `analise_financeira_projetos.py` (VPL, TIR, payback). Uma decisão de
   projeto errada (ex.: um trocador subdimensionado) limita permanentemente o que a otimização em
   tempo real consegue explorar depois.

## Por que o Economic MPC encontra um ponto diferente do setpoint "óbvio"

O resultado central da seção Economic MPC do `README.md` — o reator opera acima do setpoint fixo
tradicional (330 K) porque a receita extra da conversão mais rápida supera o custo energético
adicional, dentro da margem seguros abaixo do teto de temperatura — ilustra o princípio geral por
trás de qualquer otimização econômica de processo: o ponto operacional ótimo quase nunca coincide
com o setpoint que um engenheiro escolheria a priori por "bom senso" (ex.: o ponto médio de uma
faixa operacional) — ele emerge do trade-off real entre as curvas de custo e receita, e desloca
sempre que essas curvas mudam (preço do produto, custo de energia).
