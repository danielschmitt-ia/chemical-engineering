"""Lado do GÊMEO DIGITAL / APC na integração: um cliente OPC-UA que se conecta ao servidor
da planta (real ou, no demo, simulado), lê o estado atual, resolve um passo do MPC
(`ReatorCSTR.calcular_acao_controle`) e aciona a planta chamando o método `AvancarPasso` com
o novo setpoint da jaqueta — o mesmo padrão de integração usado por soluções comerciais de
APC (Aspen DMC3, Honeywell Profit Controller, etc.) para se conectarem a um DCS via OPC-UA.
"""

from ..config import ConfiguracaoReator
from ..modelo import ReatorCSTR
from .servidor_opcua import NOME_OBJETO, URI_NAMESPACE

from asyncua import Client


class GatewayControleOPCUA:
    def __init__(self, config: ConfiguracaoReator, endpoint: str, economico: bool = False,
                 dt_controle: float = 0.25, Hp: int = 5):
        self.reator = ReatorCSTR(config)
        self.endpoint = endpoint
        self.economico = economico
        self.dt_controle = dt_controle
        self.Hp = Hp
        self.Tj_anterior = self.reator.T0 - 10.0
        self.chute_horizonte = None
        self.historico = []

    async def rodar(self, passos: int):
        async with Client(url=self.endpoint) as client:
            idx = await client.get_namespace_index(URI_NAMESPACE)
            objetos = client.get_objects_node()
            reator_obj = await objetos.get_child([f"{idx}:{NOME_OBJETO}"])
            var_T = await reator_obj.get_child([f"{idx}:PV_Temperatura"])
            var_CA = await reator_obj.get_child([f"{idx}:PV_ConcentracaoA"])

            for i in range(passos):
                T_medido = await var_T.read_value()
                CA_medido = await var_CA.read_value()

                Tj_otimo, self.chute_horizonte = self.reator.calcular_acao_controle(
                    CA_medido, T_medido, self.Tj_anterior, chute_horizonte=self.chute_horizonte,
                    economico=self.economico, dt_mpc=self.dt_controle, Hp=self.Hp)

                # Chama a planta (real ou simulada) para avançar exatamente um passo com essa
                # ação — em vez de escrever um setpoint e torcer para o "relógio" da planta
                # ter avançado a quantidade certa de tempo simulado entre uma leitura e outra.
                T_novo, CA_novo, sis_ativo = await reator_obj.call_method(
                    f"{idx}:AvancarPasso", float(Tj_otimo))

                self.Tj_anterior = Tj_otimo
                self.historico.append({
                    "tempo": i * self.dt_controle,
                    "T": T_novo,
                    "CA": CA_novo,
                    "Tj": Tj_otimo,
                    "sis_ativo": sis_ativo,
                })

        return self.historico
