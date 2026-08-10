# 🏭 Gêmeo Digital Dinâmico e Controle Avançado de um Reator CSTR Não-Isotérmico

Este repositório contém o ecossistema completo de um **Gêmeo Digital (Digital Twin)** para um reator químico de mistura contínua (CSTR) operando sob reação exotérmica não-linear. O projeto aborda a modelagem rigorosa dos balanços de massa e energia, simulação de falhas operacionais (*thermal runaway*), controle preditivo multivariável (MPC) e sensores virtuais baseados em Aprendizado Profundo.

---

## 📐 Modelagem Matemática do Processo

A dinâmica do reator é regida por um sistema de equações diferenciais ordinárias acopladas:

### 1. Balanço de Massa do Componente $A$
$$\frac{dC_A}{dt} = \frac{F}{V}(C_{A0} - C_A) - k(T)C_A$$

### 2. Balanço de Energia Térmica
$$\frac{dT}{dt} = \frac{F}{V}(T_0 - T) + \frac{(-\Delta H_{rx}) \cdot k(T)C_A}{\rho C_p} + \frac{UA(T_j - T)}{V \rho C_p}$$

### 3. Cinética Reacional (Lei de Arrhenius)
$$k(T) = A \cdot e^{-\frac{E_a}{R \cdot T}}$$

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
   git clone [https://github.com/danielschmitt-ia/digital-twin-cstr.git](https://github.com/danielschmitt-ia/digital-twin-cstr.git)
   cd digital-twin-cstr
