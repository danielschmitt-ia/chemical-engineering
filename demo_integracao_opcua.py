"""Demonstra a arquitetura de integração com uma planta real via OPC-UA: um servidor
(a planta/DCS) e um cliente (o gateway do gêmeo digital/APC) rodando como processos
independentes, comunicando só por rede — não chamadas de função em processo, como no
main.py. É o mesmo desenho que seria usado numa implantação real (troca o servidor
simulado por um servidor OPC-UA de verdade e nenhum código do gateway muda).

Uso:
    python demo_integracao_opcua.py
"""

import asyncio

import matplotlib.pyplot as plt

from reator_digital_twin import carregar_config
from reator_digital_twin.integracao import GatewayControleOPCUA, ServidorPlantaOPCUA

ENDPOINT = "opc.tcp://127.0.0.1:4842/reator/"
DURACAO_MIN = 20.0
DT_CONTROLE = 0.25


async def main():
    config = carregar_config("configs/reator_padrao.yaml")

    print(f"🔌 Iniciando servidor OPC-UA da planta ({config.nome_planta}) em {ENDPOINT} ...")
    servidor = ServidorPlantaOPCUA(config, ENDPOINT, dt_planta=DT_CONTROLE)
    await servidor.iniciar()

    print("🔗 Conectando o gateway do gêmeo digital (cliente OPC-UA) e operando o MPC...")
    gateway = GatewayControleOPCUA(config, ENDPOINT, economico=False, dt_controle=DT_CONTROLE)
    passos = int(DURACAO_MIN / DT_CONTROLE)
    historico = await gateway.rodar(passos=passos)

    await servidor.parar()
    print(f"✅ Integração concluída: {len(historico)} ciclos de controle via OPC-UA "
          f"(leitura, otimização e comando da planta pela rede a cada ciclo).")

    tempo = [h["tempo"] for h in historico]
    T = [h["T"] for h in historico]
    CA = [h["CA"] for h in historico]
    Tj = [h["Tj"] for h in historico]

    fig, axs = plt.subplots(2, 1, figsize=(10, 8))
    axs[0].plot(tempo, T, color="purple", label="T (retornada por AvancarPasso via OPC-UA)")
    axs[0].plot(tempo, Tj, '--', color="gray", label="Tj comandado via OPC-UA (AvancarPasso)")
    axs[0].axhline(y=config.T_alvo, color="black", linestyle=":", label="Setpoint")
    axs[0].set_title("Controle em malha fechada via OPC-UA (servidor e cliente reais, processos separados)")
    axs[0].legend(); axs[0].grid(True)

    axs[1].plot(tempo, CA, label="C_A (retornada por AvancarPasso via OPC-UA)")
    axs[1].set_title("Concentração de A lida da planta simulada")
    axs[1].set_xlabel("Tempo (min)")
    axs[1].legend(); axs[1].grid(True)

    fig.tight_layout()
    fig.savefig("integracao_opcua.png", dpi=150)
    print("📊 Figura salva em integracao_opcua.png")


if __name__ == "__main__":
    asyncio.run(main())
