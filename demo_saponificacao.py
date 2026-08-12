"""Demonstra o modo de falha por saponificação (formação de sabão), específico de
processos de transesterificação alcalina — ver docstring de
ReatorCSTR.rodar_mpc_com_saponificacao e configs/exemplo_biodiesel.yaml.

Uso:
    python demo_saponificacao.py
"""

import numpy as np
import matplotlib.pyplot as plt

from reator_digital_twin import ReatorCSTR, carregar_config

if __name__ == "__main__":
    config = carregar_config("configs/exemplo_biodiesel.yaml")
    reator = ReatorCSTR(config)

    print(f"🧴 Simulando saponificação em {config.nome_planta}...")
    t, T, Tj, CA, atividade, residuo, tempo_deteccao = reator.rodar_mpc_com_saponificacao(tempo_total=150)
    conversao = 1 - CA / config.CA0
    if tempo_deteccao is not None:
        idx = np.searchsorted(t, tempo_deteccao)
        print(f"⚠️  Saponificação detectada em t = {tempo_deteccao:.1f} min "
              f"(conversão na detecção ≈ {conversao[idx] * 100:.0f}%)")
    else:
        print("✅ Nenhuma falha detectada no horizonte simulado.")
    print(f"💧 Conversão final: {conversao[-1] * 100:.0f}% (era ≈{conversao.max() * 100:.0f}% no pico, "
          f"antes do catalisador se esgotar)")

    fig, axs = plt.subplots(3, 1, figsize=(10, 11))

    axs[0].plot(t, conversao * 100, color="darkgoldenrod")
    axs[0].set_title("Conversão em FAME (biodiesel) — colapsa conforme o catalisador é consumido por AGL")
    axs[0].set_ylabel("Conversão (%)")
    axs[0].grid(True)

    axs[1].plot(t, atividade, color="teal", label="Atividade catalítica remanescente")
    axs[1].set_title("Desativação do Catalisador por Saponificação (AGL na matéria-prima)")
    axs[1].set_ylabel("Fração ativa")
    axs[1].legend(); axs[1].grid(True)

    axs[2].plot(t, residuo, color="crimson", label="Resíduo de concentração (EWMA)")
    axs[2].axhline(y=0.05, color="black", linestyle=":", label="Limiar de alarme")
    if tempo_deteccao is not None:
        axs[2].axvline(x=tempo_deteccao, color="red", linestyle="--", label="Falha detectada")
    axs[2].set_title("Detecção de Falha por Resíduo de Concentração")
    axs[2].set_xlabel("Tempo (min)")
    axs[2].set_ylabel("mol/L")
    axs[2].legend(); axs[2].grid(True)

    fig.tight_layout()
    fig.savefig("saponificacao.png", dpi=150)
    print("📊 Figura salva em saponificacao.png")
