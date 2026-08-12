"""Lado da PLANTA REAL na integração: um servidor OPC-UA, o mesmo protocolo exposto por
DCS/historiadores industriais (Siemens PCS7, Honeywell Experion, Emerson DeltaV, Rockwell
FactoryTalk, Yokogawa CENTUM — todos falam OPC-UA hoje). Este servidor executa a física do
reator internamente (incluindo seu próprio SIS, independente de quem estiver controlando)
e publica variáveis de processo (PVs) para monitoramento; o avanço da planta é acionado
pelo método `AvancarPasso`, chamado pelo cliente de controle (o gateway do gêmeo digital) a
cada ciclo — um padrão de sincronização em lockstep, comum em bancadas de simulação
*hardware-in-the-loop*, que evita o descasamento entre o "relógio" da planta e o ritmo
real (não-determinístico) de um controlador que resolve uma otimização a cada ciclo.
"""

import logging

from asyncua import Server, ua
from asyncua.common.methods import uamethod

from ..config import ConfiguracaoReator
from ..modelo import ReatorCSTR

logging.getLogger("asyncua").setLevel(logging.WARNING)

URI_NAMESPACE = "http://reator-digital-twin.local/opcua/"
NOME_OBJETO = "Reator001"


class ServidorPlantaOPCUA:
    def __init__(self, config: ConfiguracaoReator, endpoint: str, UA_real: float = None, dt_planta: float = 0.25,
                 usar_sis: bool = False, DeltaH_real: float = None):
        """`usar_sis=False` (padrão) evolui a planta com a cinética nominal via RK4, igual
        ao MPC em processo (`rodar_mpc`) — o modo certo para demonstrar rastreamento de
        setpoint normal. `usar_sis=True` liga a camada de proteção independente (mesmo
        cenário de `simular_interlock_seguranca`): a planta passa a seguir `DeltaH_real`
        (cinética de pior caso) e o SIS pode intervir — não é o cenário de operação normal,
        já que `T_trip_sis` fica abaixo do setpoint usual de rastreamento (330 K)."""
        self.reator = ReatorCSTR(config)
        self.endpoint = endpoint
        self.UA_real = self.reator.UA_nominal if UA_real is None else UA_real
        self.dt_planta = dt_planta
        self.usar_sis = usar_sis
        self.DeltaH_real = DeltaH_real if DeltaH_real is not None else self.reator.DeltaH
        self.CA = self.reator.CA_inicial
        self.T = self.reator.T_inicial
        self.server = None

    async def iniciar(self):
        self.server = Server()
        await self.server.init()
        self.server.set_endpoint(self.endpoint)
        idx = await self.server.register_namespace(URI_NAMESPACE)
        objetos = self.server.get_objects_node()
        reator_obj = await objetos.add_object(idx, NOME_OBJETO)

        self.var_T = await reator_obj.add_variable(idx, "PV_Temperatura", float(self.T))
        self.var_CA = await reator_obj.add_variable(idx, "PV_ConcentracaoA", float(self.CA))
        self.var_UA = await reator_obj.add_variable(idx, "PV_UA_Real", float(self.UA_real))
        self.var_sp_Tj = await reator_obj.add_variable(idx, "SP_TemperaturaJaqueta",
                                                          float(self.reator.T0 - 10.0))
        self.var_alarme = await reator_obj.add_variable(idx, "ALM_SIS_Ativo", False)

        @uamethod
        async def _avancar_passo(parent, Tj_comandado):
            if self.usar_sis:
                # A planta tem seu próprio SIS, hard-wired, independente de qualquer
                # controlador externo conectado — ver modelo.ReatorCSTR._avancar_com_sis.
                self.CA, self.T, sis_ativo = self.reator._avancar_com_sis(
                    self.CA, self.T, Tj_comandado, self.UA_real, self.dt_planta, self.DeltaH_real)
            else:
                self.CA, self.T = self.reator._rk4_step(
                    self.CA, self.T, Tj_comandado, self.UA_real, self.dt_planta)
                sis_ativo = False
            await self.var_T.write_value(float(self.T))
            await self.var_CA.write_value(float(self.CA))
            await self.var_sp_Tj.write_value(float(Tj_comandado))
            await self.var_alarme.write_value(bool(sis_ativo))
            return float(self.T), float(self.CA), bool(sis_ativo)

        await reator_obj.add_method(
            idx, "AvancarPasso", _avancar_passo,
            [ua.VariantType.Double],
            [ua.VariantType.Double, ua.VariantType.Double, ua.VariantType.Boolean])

        await self.server.start()

    async def parar(self):
        if self.server is not None:
            await self.server.stop()
