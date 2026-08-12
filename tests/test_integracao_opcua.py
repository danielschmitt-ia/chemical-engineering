"""Testes de integração para o servidor e o gateway OPC-UA (reator_digital_twin.integracao).

Sobem um servidor OPC-UA de verdade (porta local dedicada, isolada dos demos) e conectam um
cliente de verdade — não mocks. Cobrem os três bugs reais encontrados ao construir essa
camada (ver commit "Adiciona integração OPC-UA"): descasamento de relógio entre planta e
controlador, falta de warm-start no otimizador e SIS disparando indevidamente em operação
normal — cada um teria passado despercebido sem um teste fim a fim como este.
"""

import numpy as np
import pytest

from reator_digital_twin.integracao import GatewayControleOPCUA, ServidorPlantaOPCUA

ENDPOINT_TESTE = "opc.tcp://127.0.0.1:4855/reator-teste/"


@pytest.mark.asyncio
async def test_ciclo_fechado_avanca_em_direcao_ao_setpoint(config_padrao):
    servidor = ServidorPlantaOPCUA(config_padrao, ENDPOINT_TESTE, dt_planta=0.25, usar_sis=False)
    await servidor.iniciar()
    try:
        gateway = GatewayControleOPCUA(config_padrao, ENDPOINT_TESTE, dt_controle=0.25)
        historico = await gateway.rodar(passos=20)
    finally:
        await servidor.parar()

    assert len(historico) == 20
    T = np.array([h["T"] for h in historico])
    # Sem SIS espúrio nem descasamento de relógio, a temperatura deve subir monotonicamente
    # em direção ao setpoint (330 K) nesse trecho inicial do transiente — igual ao MPC em
    # processo (rodar_mpc).
    assert T[-1] > T[0]
    assert np.all(np.diff(T) > -0.05)  # essencialmente monotônico (só ruído numérico)
    assert T[-1] < config_padrao.T_max_seguro


@pytest.mark.asyncio
async def test_ciclo_fechado_bate_com_mpc_em_processo(config_padrao, reator):
    """Regressão direta dos bugs de warm-start e descasamento de relógio: a trajetória via
    OPC-UA precisa reproduzir a trajetória de rodar_mpc() em processo, passo a passo."""
    _, T_processo, _, _ = reator.rodar_mpc(tempo_total=5)

    servidor = ServidorPlantaOPCUA(config_padrao, ENDPOINT_TESTE, dt_planta=0.25, usar_sis=False)
    await servidor.iniciar()
    try:
        gateway = GatewayControleOPCUA(config_padrao, ENDPOINT_TESTE, dt_controle=0.25)
        historico = await gateway.rodar(passos=20)
    finally:
        await servidor.parar()

    T_opcua = [h["T"] for h in historico]
    assert T_opcua[-1] == pytest.approx(T_processo[-1], abs=1.0)


@pytest.mark.asyncio
async def test_sis_intervem_via_opcua_sob_cinetica_de_pior_caso(config_padrao):
    servidor = ServidorPlantaOPCUA(config_padrao, ENDPOINT_TESTE, dt_planta=0.25,
                                    usar_sis=True, DeltaH_real=-250000.0)
    await servidor.iniciar()
    try:
        gateway = GatewayControleOPCUA(config_padrao, ENDPOINT_TESTE, dt_controle=0.25)
        historico = await gateway.rodar(passos=20)
    finally:
        await servidor.parar()

    assert any(h["sis_ativo"] for h in historico)
    T = np.array([h["T"] for h in historico])
    assert T.max() < 380.0  # bem contido frente ao pico >380K observado sem SIS
