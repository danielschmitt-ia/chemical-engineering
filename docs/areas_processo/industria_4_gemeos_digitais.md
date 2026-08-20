# Indústria 4.0 e Gêmeos Digitais

Este item não vira um módulo separado porque **este repositório inteiro é o exemplo concreto**:
`reator_digital_twin/` é um gêmeo digital dinâmico completo de um reator CSTR — modelagem física
rigorosa, controle avançado (MPC/Economic MPC), sensores virtuais (soft sensors por ensemble de
redes neurais), detecção de falha por resíduo, uma camada de proteção independente conceitual
(SIS) e integração via OPC-UA com um DCS/historiador simulado. Ver o `README.md` principal e
`docs/PROJETO_INDUSTRIAL.md` (arquitetura, roadmap de simulação → shadow mode → piloto →
produção) para o tratamento completo.

## O que caracteriza um gêmeo digital (vs. uma simulação offline)

- **Sincronizado com a planta real** (ou, aqui, com o servidor OPC-UA que representa o DCS) — não
  roda isolado, mas troca dados continuamente com o processo físico.
- **Bidirecional** — não só observa (soft sensor, detecção de falha), mas também atua (o gateway
  MPC resolve a ação de controle e escreve de volta na planta).
- **Mantém-se consistente com a realidade ao longo do tempo** — por isso a detecção de falha por
  resíduo (fouling do UA, desativação catalítica por saponificação) é uma peça central: um gêmeo
  digital cujo modelo diverge silenciosamente da planta real (descasamento de modelo) deixa de
  cumprir sua função, e pior, pode mascarar essa divergência enquanto o MPC ainda consegue atingir
  o setpoint (ver a seção "Detecção de Falha por Resíduo" do README).

## Onde a "Indústria 4.0" mais ampla entra

O gêmeo digital de um único reator é a unidade básica; a visão de Indústria 4.0 estende o mesmo
princípio (sincronização contínua entre modelo e planta física, mais automação e menos
intervenção manual) para a fábrica inteira — integração entre PIMS (`pims_patrimonio_dados.md`),
MES (manufacturing execution system), planejamento de produção (`pcp_planejamento_producao.md`,
Área 10) e manutenção preditiva (`manutencao_preditiva_proativa.md`, Área 8), todos alimentados
pelo mesmo tipo de dado de processo em tempo real.
