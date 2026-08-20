"""Instrumentação e controle de processos: o controlador PID (proporcional-integral-derivativo),
o algoritmo de controle de malha fechada mais usado na indústria de processos — a base sobre a
qual o MPC de `reator_digital_twin/modelo.py` melhora quando restrições e um modelo de processo
explícito compensam suas limitações (ver `docs/areas_processo/mpc.md`).
"""


def parametros_isa_para_paralelo(Kp: float, Ti: float, Td: float) -> tuple[float, float, float]:
    """Converte os parâmetros de sintonia na forma ISA padrão (ganho proporcional Kp, tempo
    integral Ti, tempo derivativo Td — a forma em que a maioria dos DCS/PLCs pede a sintonia)
    para a forma paralela (Kp, Ki, Kd) usada em `saida_pid_paralelo`:

        Ki = Kp/Ti,  Kd = Kp·Td

    `Ti` e `Td` na mesma unidade de tempo de `dt` em `saida_pid_paralelo`."""
    return Kp, Kp / Ti, Kp * Td


def saida_pid_paralelo(Kp: float, Ki: float, Kd: float, erro: float, integral_erro: float,
                        erro_anterior: float, dt: float) -> float:
    """Saída de um controlador PID na forma paralela (posicional):

        u = Kp·e + Ki·∫e·dt + Kd·(e - e_anterior)/dt

    O termo integral (`integral_erro`) é acumulado pelo chamador entre chamadas sucessivas (ex.:
    `integral_erro += erro * dt` a cada passo, antes de chamar esta função) — esta função não
    mantém estado interno, na mesma linha funcional do resto do pacote; cabe ao chamador também
    implementar proteção contra windup (ex.: saturar `integral_erro` quando a saída satura no
    limite do atuador) se necessário. `erro = setpoint - variável_de_processo`."""
    termo_proporcional = Kp * erro
    termo_integral = Ki * integral_erro
    termo_derivativo = Kd * (erro - erro_anterior) / dt
    return termo_proporcional + termo_integral + termo_derivativo
