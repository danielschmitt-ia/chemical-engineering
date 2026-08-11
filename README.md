# 🏭 Gêmeo Digital Dinâmico e Controle Avançado de um Reator CSTR Não-Isotérmico

Este repositório contém o ecossistema completo de um **Gêmeo Digital (Digital Twin)** para um reator químico de mistura contínua (CSTR) operando sob reação exotérmica não-linear. O projeto aborda a modelagem rigorosa dos balanços de massa e energia, simulação de falhas operacionais (*thermal runaway*), controle preditivo multivariável (MPC) com restrições de segurança, sensores virtuais baseados em Aprendizado Profundo e detecção de falhas por resíduo.

---

## 📐 Modelagem Matemática do Processo

A dinâmica do reator é regida por um sistema de equações diferenciais ordinárias acopladas:

### 1. Balanço de Massa do Componente $A$
$$\frac{dC_A}{dt} = \frac{F}{V}(C_{A0} - C_A) - k(T)C_A$$

### 2. Balanço de Energia Térmica
$$\frac{dT}{dt} = \frac{F}{V}(T_0 - T) + \frac{(-\Delta H_{rx}) \cdot k(T)C_A}{\rho C_p} + \frac{UA(T_j - T)}{V \rho C_p}$$

### 3. Cinética Reacional (Lei de Arrhenius)
$$k(T) = A \cdot e^{-\frac{E_a}{R \cdot T}}$$

### 4. Integração Numérica

As equações são integradas com métodos adequados a cada uso: **RK45 adaptativo** (`scipy.integrate.solve_ivp`) na análise de fuga térmica em malha aberta, onde a dinâmica se torna rígida (*stiff*) perto do runaway; e **RK4 de passo fixo** dentro do MPC, que equilibra precisão e custo computacional determinístico exigido por um controlador em tempo real.

---

## 🛡️ Segurança e Confiabilidade

### MPC com Restrições de Segurança
Além de perseguir o setpoint, o controlador preditivo respeita duas restrições explícitas, impostas ao otimizador via `NonlinearConstraint`:
- **Teto de temperatura** (`T_max_seguro`): a trajetória prevista ao longo do horizonte não pode ultrapassar o limite térmico seguro do reator.
- **Limite de taxa do atuador** (`taxa_max_Tj`): a temperatura da jaqueta não pode variar além de um valor máximo por passo de controle, refletindo a dinâmica real do atuador.

### Detecção de Falha por Resíduo (Fouling do UA)
O gêmeo digital também monitora a saúde do processo: um cenário dedicado simula a incrustação progressiva (*fouling*) da superfície de troca térmica, reduzindo gradualmente o coeficiente `UA` real da planta enquanto o modelo do MPC continua assumindo o valor nominal. Um detector por resíduo (média móvel exponencial do erro entre a temperatura medida e a prevista pelo modelo) sinaliza a degradação **antes** que ela se torne um evento de segurança — mesmo quando o MPC ainda consegue manter a temperatura no setpoint, mascarando o sintoma.

---

## 📊 Resultados da Simulação

### 1. Análise de Fuga Térmica (*Thermal Runaway*)
Avaliação de risco em malha aberta demonstrando como uma queda de eficiência no coeficiente de troca térmica ($UA$) provoca a disparada de temperatura no reator:

![Estabilidade e Runaway Térmico](estabilidade_runaway.png)

### 2. Controle Preditivo (MPC) e Soft Sensor (Rede Neural)
Desempenho da malha fechada mantendo o reator no setpoint estipulado ($330\text{ K}$) enquanto a Rede Neural (MLP) estima a concentração de saída $C_A$ em tempo real com alta precisão:

![Desempenho do MPC e Soft Sensor](mpc_softsensor.png)

---

## ⚙️ Como Executar o Projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/danielschmitt-ia/digital-twin-cstr.git
   cd digital-twin-cstr
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Execute a simulação integrada:
   ```bash
   python main.py
   ```

   O script imprime no console o instante em que uma eventual falha de fouling é detectada e exibe 5 gráficos: fuga térmica, desempenho do MPC com restrições de segurança, soft sensor, degradação simulada do `UA` e o resíduo usado na detecção de falha.
