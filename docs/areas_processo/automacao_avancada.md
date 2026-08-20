# Automação Avançada

"Automação avançada" (APC — Advanced Process Control, no jargão da indústria) é o guarda-chuva
que cobre tudo que vai além do controle regulatório básico (PID) de uma malha isolada — MPC
multivariável (`docs/areas_processo/mpc_controle_preditivo.md`), controle inferencial (soft
sensors — ver `mpc_softsensor.png` e o ensemble de redes neurais do `reator_digital_twin`),
otimização em tempo real (RTO) e controle de restrições. Não é tratado como cálculo isolado
porque, na prática, é a integração de várias das outras peças deste repositório (MPC, soft
sensors, detecção de falha) em uma arquitetura de controle hierárquica — não uma fórmula única.

## A hierarquia típica de controle em uma planta

1. **Regulatório (PID)** — a base: controla vazão, nível, pressão, temperatura em malhas
   individuais (`controle_pid.py`). Roda a cada segundo ou mais rápido.
2. **Avançado/multivariável (MPC)** — coordena várias malhas regulatórias simultaneamente,
   respeitando restrições de processo e otimizando um objetivo (setpoint ou econômico — ver
   `mpc_controle_preditivo.md`). Roda tipicamente a cada 15s-5min, dependendo da dinâmica do
   processo.
3. **Otimização em tempo real (RTO)** — ajusta os setpoints/alvos que o MPC persegue, com base em
   um modelo de processo em regime permanente (rigoroso ou empírico) que busca o ponto ótimo
   econômico da planta inteira. Roda tipicamente a cada hora ou por turno.
4. **Planejamento e agendamento** — decide o que produzir e quando, no nível do site ou da
   empresa (ver `docs/areas_processo/pcp_planejamento_producao.md`). Roda diariamente/semanalmente.

## Por que essa hierarquia (e não um único otimizador global)

Cada camada opera em uma escala de tempo diferente e com um nível de detalhe de modelo diferente
— tentar resolver tudo em um único otimizador monolítico seria computacionalmente inviável e
frágil a mudanças (uma câmera trocada, uma malha em manual). A hierarquia isola a complexidade: a
camada rápida (PID) garante estabilidade básica mesmo se a camada lenta (RTO) estiver fora do ar;
a camada lenta corrige o alvo da camada rápida sem precisar conhecer sua dinâmica detalhada.
