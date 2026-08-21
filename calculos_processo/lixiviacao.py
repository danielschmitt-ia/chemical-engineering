"""Lixiviação e extração sólido-líquido: modelo de estágio ideal (o soluto solúvel se dissolve
por completo e se distribui uniformemente no líquido do estágio — overflow e o líquido retido
pelo sólido no underflow saem com a mesma concentração), a mesma aproximação usada para o método
clássico de subcorrente constante (constant underflow) em lixiviação em múltiplos estágios.
"""


def concentracao_lixiviado(massa_soluto_dissolvido: float, massa_liquido_total: float) -> float:
    """Concentração do soluto no líquido de um estágio ideal de lixiviação (assumindo
    dissolução completa do soluto solúvel disponível): c = massa_soluto/massa_líquido_total."""
    return massa_soluto_dissolvido / massa_liquido_total


def rendimento_lixiviacao_estagio_ideal(massa_solvente: float, massa_liquido_retido_solido: float) -> float:
    """Fração do soluto recuperada no líquido sobrenadante (overflow) de um único estágio ideal
    de lixiviação, com o sólido de alimentação entrando seco (sem líquido) e todo o soluto
    solúvel se dissolvendo uniformemente no solvente adicionado:

        rendimento = (massa_solvente - massa_líquido_retido) / massa_solvente

    Como a concentração é uniforme no estágio ideal, essa fração não depende de quanto soluto
    havia na alimentação — só de que fração do líquido total sai como overflow em vez de ficar
    retida no underflow. `massa_liquido_retido_solido`: massa de líquido retida nos
    poros/interstícios do sólido no underflow (propriedade do sólido e do equipamento — maior
    para tortas mais finas ou compressíveis). Assume solvente suficiente para dissolver todo o
    soluto disponível (senão, uma fração permanece como sólido não dissolvido, fora do escopo
    deste modelo de estágio ideal)."""
    if massa_liquido_retido_solido >= massa_solvente:
        raise ValueError("massa_liquido_retido_solido não pode exceder massa_solvente")
    return (massa_solvente - massa_liquido_retido_solido) / massa_solvente
