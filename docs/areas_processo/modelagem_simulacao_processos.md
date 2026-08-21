# Modelagem e Simulação de Processos

Não é um módulo separado porque **este repositório inteiro é o estudo de caso**: o gêmeo digital
do CSTR em `reator_digital_twin/modelo.py` é uma modelagem rigorosa de processo — balanços de
massa e energia (EDOs acopladas), integração numérica escolhida por adequação a cada regime
(RK45 adaptativo perto do runaway térmico, onde a dinâmica é rígida/stiff; RK4 de passo fixo
dentro do MPC, onde o custo computacional determinístico importa mais) e validação contra
comportamento físico esperado (ver `tests/test_modelo.py`).

## Por que a escolha do integrador numérico importa

A escolha entre um integrador adaptativo (RK45, `scipy.integrate.solve_ivp`) e um de passo fixo
(RK4 implementado manualmente em `modelo.py`) não é incidental — reflete um trade-off real:

- **RK45 adaptativo**: ajusta o passo automaticamente para manter a precisão, essencial perto do
  runaway térmico (`simular_runaway`), onde a dinâmica muda de escala de tempo rapidamente
  (rígida/stiff) e um passo fixo perderia precisão ou exigiria um passo tão pequeno que o custo
  computacional explodiria.
- **RK4 de passo fixo**: mais previsível em custo computacional — importante dentro do laço do
  MPC (`_rollout_mpc`), chamado repetidamente a cada iteração do otimizador, onde um tempo de
  execução determinístico é mais valioso que a adaptação automática de passo.

## Outras técnicas de modelagem de processo (fora do escopo deste repositório)

- **Simulação em regime permanente com reciclo** (ex.: Aspen Plus, DWSIM) — resolve fluxogramas
  inteiros com correntes de reciclo via métodos iterativos (Wegstein, Broyden), fora do escopo de
  um único reator dinâmico como o deste repositório.
- **Simulação estocástica/Monte Carlo** — propagação de incerteza através de um modelo de
  processo, relacionada ao ensemble de redes neurais usado aqui para o soft sensor (que já captura
  incerteza de forma similar, por dispersão entre modelos).
