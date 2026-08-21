# Controle Preditivo Baseado em Modelo (MPC)

Não é um novo módulo em `calculos_processo/` porque este repositório já tem uma implementação
completa, testada e documentada de MPC: `reator_digital_twin/modelo.py`, na classe `ReatorCSTR`.

## O que já existe aqui

- **`calcular_acao_controle()`** — resolve um único passo do MPC a partir do estado medido (a
  interface que a integração em tempo real via OPC-UA usa), com *warm-start* do otimizador entre
  chamadas sucessivas.
- **`rodar_mpc()`** — MPC de rastreamento de setpoint, com restrição de segurança de temperatura
  (`NonlinearConstraint`) e limite de taxa do atuador.
- **`rodar_mpc_economico()`** — Economic MPC: substitui o custo de rastreamento por um custo
  econômico direto (receita de conversão menos custo energético), mantendo as mesmas restrições
  de segurança.
- **`_otimizar()`** — o núcleo do MPC: otimização não-linear restrita via SLSQP
  (`scipy.optimize.minimize`), com as restrições de teto de temperatura e taxa do atuador
  impostas explicitamente.

Ver a seção "MPC com Restrições de Segurança" e "Economic MPC" do
[`README.md`](../../README.md) principal, e os testes em `tests/test_modelo.py`
(`TestMPCRastreamento`, `TestMPCEconomico`, `TestCalcularAcaoControle`) para exemplos de uso e a
verificação de que as restrições são de fato respeitadas.

## Por que MPC em vez de PID (`controle_pid.py`)

Um PID reage ao erro atual (e sua taxa de variação/acumulação), sem "enxergar" o futuro nem
respeitar restrições explicitamente — restrições em um PID geralmente são impostas de forma
indireta (saturação do atuador, lógica de override). Um MPC resolve, a cada passo, uma otimização
sobre um horizonte de predição usando um modelo explícito do processo, incorporando restrições de
segurança (ex.: teto de temperatura) diretamente na formulação do problema de otimização — por
isso é o padrão em unidades onde restrições operacionais apertadas tornam esse "ver à frente e
respeitar limites" valioso o suficiente para justificar a complexidade adicional (identificação de
modelo, mais poder computacional, sintonia mais elaborada) frente a um PID.
