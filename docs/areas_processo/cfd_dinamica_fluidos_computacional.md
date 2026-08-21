# Dinâmica de Fluidos Computacional (CFD)

CFD resolve numericamente as equações de Navier-Stokes (balanço de quantidade de movimento) em
uma malha espacial discretizada, junto com balanços de energia e espécies quando relevante — um
problema de EDPs (equações diferenciais parciais) em 3D, fundamentalmente diferente em escopo das
EDOs (equações diferenciais ordinárias, no tempo) que `reator_digital_twin/modelo.py` resolve para
um reator de mistura perfeita (CSTR). Por isso não é reduzido a uma fórmula fechada aqui — é uma
disciplina de solução numérica de sistemas de equações com milhões de graus de liberdade, tipicamente
resolvida em software dedicado (Ansys Fluent, OpenFOAM, Aspen CFD), não em funções fechadas.

## Por que um CSTR não precisa de CFD (e quando um processo precisa)

O modelo deste repositório assume mistura perfeita (concentração e temperatura uniformes em todo
o volume do reator) — uma simplificação razoável quando a agitação é vigorosa o suficiente para
que os gradientes espaciais sejam desprezíveis frente à dinâmica temporal que importa (a cinética
de reação, o controle). CFD se torna necessário quando essa suposição falha e os gradientes
espaciais são o próprio fenômeno de interesse:

- **Zonas mortas e curto-circuito de mistura** em tanques mal agitados ou reatores tubulares com
  escoamento não-ideal.
- **Distribuição de temperatura não-uniforme** em um reator de leito fixo grande (relevante para
  os hot spots que motivam parte da análise de segurança deste repositório em uma geometria real).
- **Escoamento multifásico** (gás-líquido em uma coluna de bolhas, sólido-líquido em uma
  suspensão) onde a interação entre fases não é capturada por um balanço macroscópico.
- **Projeto de geometria de equipamento** (posição de bicos, chicanas, distribuidores) onde a
  forma física do escoamento é a variável de projeto.

## Como isso se conecta com os módulos deste pacote

CFD tipicamente fornece os parâmetros efetivos que os modelos macroscópicos (como os deste
repositório) tratam como entrada — ex.: o coeficiente de troca térmica U de
`transferencia_calor.py`, ou a difusividade efetiva usada no módulo de Thiele
(`reatores_leito_fixo.modulo_thiele_esfera`), podem vir de uma simulação CFD detalhada em vez de
uma correlação de bancada, quando a geometria real do equipamento se desvia muito dos casos
padronizados que essas correlações assumem.
