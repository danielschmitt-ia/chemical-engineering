"""Pirólise e gaseificação de resíduos: eficiência de gás frio (cold gas efficiency), a métrica
central de desempenho de um gaseificador — quanto da energia química da biomassa/resíduo
alimentado termina como energia química no gás de síntese produzido, em vez de perdida como calor
sensível do gás quente, char não convertido, ou alcatrão."""


def eficiencia_gas_frio(massa_gas: float, pci_gas: float, massa_biomassa: float, pci_biomassa: float) -> float:
    """Eficiência de gás frio (cold gas efficiency, CGE): razão entre a energia química
    carregada pelo gás de síntese produzido e a energia química da biomassa/resíduo alimentado —

        CGE = (massa_gás·PCI_gás) / (massa_biomassa·PCI_biomassa)

    Chamada "gás frio" porque considera só a energia química do gás (seu PCI), não o calor
    sensível que ele carrega na temperatura de saída do gaseificador — esse calor sensível
    tipicamente é recuperado à parte (ex.: gerando vapor) e contabilizado separadamente na
    eficiência global da planta. CGE tipicamente na faixa de 60-90% para gaseificadores bem
    projetados; a diferença para 100% vai para char não convertido, alcatrão e perdas térmicas do
    próprio reator."""
    return (massa_gas * pci_gas) / (massa_biomassa * pci_biomassa)
