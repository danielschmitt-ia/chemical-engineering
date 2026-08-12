# Projeto Industrial: Gêmeo Digital e APC para Reator CSTR Exotérmico

**Status:** conceitual — arquitetura, código e integração validados em simulação; nenhuma
etapa de comissionamento com dados de planta real ou hardware de segurança certificado foi
executada. Este documento é o roteiro para levar este repositório de demonstração a uma
implantação industrial real.

---

## 1. Resumo Executivo

Este repositório evoluiu de uma simulação didática para um **gêmeo digital modular e
configurável**: modelo físico, controle preditivo (MPC de rastreamento e econômico),
detecção de falha por resíduo, uma camada de proteção independente (SIS) e uma interface de
integração via OPC-UA — o protocolo padrão da indústria para conectar aplicações a um
DCS/historiador real (Siemens PCS7, Honeywell Experion, Emerson DeltaV, Rockwell
FactoryTalk, Yokogawa CENTUM).

A proposta deste documento é definir o que falta, em ordem, para sair de "roda em
simulação" para "roda numa planta real" — sem pular etapas de comissionamento e validação
que a segurança de processo exige.

## 2. Contexto e Problema de Negócio

Aplicação-alvo ilustrativa (ver `configs/exemplo_planta_industrial.yaml`): um reator CSTR de
**química fina/especialidades** (ex.: nitração, oxidação, hidrogenação, esterificação —
processos usados em agroquímicos, intermediários farmacêuticos e aditivos industriais),
operando com reação exotérmica e histórico de incidentes reais do setor (T2 Laboratories
2007, Synthron 2006 — ver README, seção "Aplicações Industriais").

Dores de negócio que a solução ataca:

| Dor | Módulo deste projeto |
|---|---|
| Setpoint fixo escolhido por regra de bolso, sem otimizar economicamente | Economic MPC |
| Perda de resfriamento sem aviso prévio até virar evento de segurança | Detecção de falha por resíduo (FDI) |
| Restrições de segurança do MPC dependem do modelo, que pode estar errado | SIS (camada independente) |
| Analisador em linha caro/lento para medir concentração | Soft sensor com incerteza (ensemble) |
| Integração com sistemas de controle historicamente cara e proprietária | Gateway OPC-UA (protocolo aberto e padrão de mercado) |

## 3. Arquitetura da Solução

```
┌─────────────────────────────┐        OPC-UA         ┌──────────────────────────────┐
│   DCS / Historiador real    │◄──────────────────────►│  Gateway do Gêmeo Digital     │
│   (ou, em demo, o servidor  │   PV_Temperatura        │  (reator_digital_twin.       │
│   simulado deste repo)      │   PV_ConcentracaoA      │   integracao.gateway_opcua)   │
│                              │   SP_TemperaturaJaqueta │                                │
│  - Sensores/atuadores reais │   Método AvancarPasso   │  - MPC de rastreamento        │
│  - SIS FÍSICO, certificado  │                          │  - Economic MPC               │
│    (IEC 61511) — obrigatório│                          │  - Detecção de falha (FDI)    │
│    e independente do        │                          │  - Soft sensor (ensemble)     │
│    software deste repo      │                          │                                │
└─────────────────────────────┘                          └──────────────────────────────┘
```

- `reator_digital_twin/config.py` — parâmetros de planta em YAML (`configs/`), nunca
  hardcoded; cada planta real usa seu próprio arquivo, calibrado a partir de dados dela.
- `reator_digital_twin/modelo.py` — física do reator, MPC e SIS; testado em
  `main.py` (simulações de ponta a ponta) e via a interface `calcular_acao_controle`
  (um passo por vez, a que a integração usa).
- `reator_digital_twin/integracao/` — servidor (representa a planta/DCS) e gateway
  (representa o nó de APC) OPC-UA; ver `demo_integracao_opcua.py`.

### ⚠️ Sobre o módulo de SIS deste repositório

O SIS implementado aqui (`ReatorCSTR._avancar_com_sis`, `simular_interlock_seguranca`)
demonstra o **princípio** de uma camada de proteção independente (IEC 61511) — é uma
ferramenta pedagógica de simulação, **não um Sistema Instrumentado de Segurança
certificado**. Um SIS real exige lógica em hardware com SIL avaliado (IEC 61508/61511),
sensores e atuadores dedicados e fisicamente independentes do BPCS/APC, testes de prova
periódicos e um LOPA/SIL assessment formal. Nenhuma implantação real deste projeto deve
substituir o SIS físico da planta pelo código Python deste repositório — o software aqui
serve para *desenhar e validar a lógica de proteção* antes de especificar o hardware real.

## 4. Roadmap de Implantação

| Fase | Objetivo | Critério de saída |
|---|---|---|
| **0 — Simulação (concluída)** | Validar a arquitetura, o MPC, a detecção de falha, o SIS conceitual e a integração OPC-UA em ambiente 100% simulado | Este repositório |
| **1 — Comissionamento do modelo** | Estimar `Pre_exp_A`, `Ea_R`, `DeltaH`, `UA` reais a partir de dados históricos da planta-alvo (regressão não-linear, dados de batelada/campanha); validar contra dados que o modelo não viu | Erro de previsão do modelo dentro de uma faixa aceitável definida com o time de processo |
| **2 — Shadow mode** | Gêmeo digital conectado ao histórico real via OPC-UA (read-only), soft sensor e detecção de falha rodando em paralelo à operação normal, sem atuar | Alarmes/estimativas do gêmeo digital revisados por operadores/engenharia de processo por um período definido (ex.: um trimestre), sem falsos positivos inaceitáveis |
| **3 — PHA/LOPA formal e especificação do SIS físico** | Rodar HAZOP/LOPA formal usando os cenários deste repositório como ponto de partida; especificar o SIS físico (SIL, sensores/atuadores dedicados) | PHA assinado pelo time de segurança de processo; SIS físico especificado e (se necessário) instalado |
| **4 — Piloto em malha fechada, escopo limitado** | MPC de rastreamento atuando de fato, com supervisão humana constante e SIS físico já instalado; Economic MPC ainda em modo assessoria (sugere, não atua) | Desempenho igual ou superior ao controle anterior, sem intervenções de segurança inesperadas |
| **5 — Produção plena** | Economic MPC em malha fechada; detecção de falha alimentando manutenção preditiva; integração plena com o historiador | Acordado com operação e segurança de processo como critério de aceite final |

**Não pule fases.** Cada uma existe porque uma falha nela é exatamente o tipo de causa raiz
documentada nos incidentes reais citados no README (modelo não validado, ausência de PHA,
ausência de camada de proteção independente).

## 5. Requisitos Técnicos para Produção

- **Conectividade**: servidor OPC-UA real exposto pelo DCS/historiador (a maioria dos
  sistemas modernos já expõe; sistemas legados podem precisar de um gateway OPC-UA/Modbus).
- **Segurança cibernética**: política de segurança OPC-UA com certificados (não
  `SecurityPolicy.NoSecurity`, usado só no demo local deste repositório), segmentação de
  rede (o gateway do gêmeo digital não deve ter acesso direto a equipamentos de campo, só
  ao servidor OPC-UA), controle de acesso e auditoria de escrita de setpoints.
- **SIS físico**: independente do software deste projeto (ver seção 3).
- **Infraestrutura de cômputo**: o gateway pode rodar em qualquer máquina da rede de
  planta (não precisa estar no mesmo host do DCS); requisitos modestos (a otimização SLSQP
  usada aqui roda em ~0.1 s por ciclo de controle neste hardware de referência).
- **Historiador**: acesso de leitura para a fase de comissionamento (estimação de
  parâmetros) e shadow mode.

## 6. Caso de Negócio (ilustrativo)

Os números abaixo são **ilustrativos**, para orientar a conversa com o time de operações —
não são uma estimativa de ROI calibrada para uma planta específica:

- **Economic MPC vs. setpoint fixo**: no cenário demonstrado (`economic_mpc.png`), operar no
  ponto ótimo encontrado automaticamente (~336 K) em vez do setpoint fixo (330 K) aumentou o
  lucro simulado em ~15% no horizonte testado, sem violar nenhuma restrição de segurança.
- **Detecção de falha antecipada**: no cenário de fouling (`deteccao_falha.png`), a
  degradação do `UA` foi sinalizada ~13 minutos antes de o MPC perder a capacidade de manter
  o setpoint — em escala de planta real, isso pode significar dias ou semanas de
  antecedência para agendar limpeza de trocador antes de uma parada não-planejada.
- **Custo evitado de incidente**: o próprio texto do README lista o custo de dois
  incidentes reais de fuga térmica (T2 Laboratories, Synthron) — na casa de vidas humanas e
  dezenas de milhões de dólares em danos. Uma camada de proteção independente bem
  especificada é, por definição de LOPA, dimensionada para reduzir a frequência desse tipo
  de evento a um nível tolerável.

## 7. Riscos e Mitigações

| Risco | Mitigação |
|---|---|
| Descasamento modelo-planta (o que a Fase 1 existe para reduzir, mas nunca elimina) | SIS físico independente do modelo (não confia na precisão do modelo para proteger a planta) |
| Resistência operacional / falta de confiança no controlador | Fase 3-4 com supervisão humana constante e critérios de aceite explícitos antes de avançar |
| Ciberssegurança da integração OPC-UA | Segmentação de rede, certificados, política de segurança adequada (ver seção 5) |
| Mudança de matéria-prima/catalisador alterando a cinética real | Refazer a Fase 1 (reestimação de parâmetros) sempre que a química do processo mudar |

## 8. Próximos Passos Técnicos

1. Escolher a planta-alvo real e coletar dados históricos (temperatura, vazões, amostras de
   laboratório) para a Fase 1.
2. Adicionar testes automatizados (`pytest`) cobrindo os módulos de `reator_digital_twin/`,
   hoje validados só por execução manual — pré-requisito antes de qualquer uso além de
   demonstração.
3. Trocar o `NoSecurity` do demo OPC-UA por uma política de segurança real
   (certificado X.509) antes de conectar a qualquer rede que não seja um laboratório
   isolado.
4. Envolver o time de segurança de processo desde a Fase 1, não só na Fase 3 — o desenho
   dos cenários de risco deste repositório deve ser revisado por quem vai assinar o PHA.
