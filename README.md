# 🏭 Gêmeo Digital Dinâmico e Controle Avançado de um Reator CSTR Não-Isotérmico

Este repositório contém um ecossistema completo de **Engenharia de Processos Industrial (Indústria 4.0)** desenvolvido em Python. O projeto fornece a física real de um reator de mistura contínua (CSTR) operando uma reação altamente exotérmica, simulando riscos térmicos, controle avançado preditivo e sensores virtuais inteligentes baseados em Deep Learning.

## 📐 Fundamentos Teóricos e Modelagem Matemática

O sistema é governado por equações diferenciais ordinárias acopladas e não-lineares, representando os balanços dinâmicos de massa e energia na planta.

### 1. Balanço de Massa (Componente A)
$$\frac{dC_A}{dt} = \frac{F}{V}(C_{A0} - C_A) - k(T)C_A$$

### 2. Balanço de Energia
$$\frac{dT}{dt} = \frac{F}{V}(T_0 - T) + \frac{(-\Delta H_{rx}) \cdot k(T)C_A}{\rho C_p} + \frac{UA(T_j - T)}{V \rho C_p}$$

### 3. Dependência Cinética (Lei de Arrhenius)
$$k(T) = A \cdot e^{-\frac{E_a}{RT}}$$
