"""Válvulas de controle e elementos finais: a equação do coeficiente de vazão (Cv) — o
dimensionamento padrão de uma válvula de controle em serviço líquido, escoamento turbulento não
crítico (sem cavitação/flashing) — e as duas características de válvula mais comuns (linear e
igual-percentagem), que definem como a vazão responde ao curso da válvula.
"""


def vazao_valvula_controle(Cv: float, delta_P: float, densidade_relativa: float) -> float:
    """Vazão através de uma válvula de controle em serviço líquido, regime turbulento não
    crítico: Q = Cv·√(ΔP/SG). `Cv`: coeficiente de vazão da válvula na abertura atual (USGPM por
    √psi, convenção ISA/ANSI padrão); `delta_P`: queda de pressão na válvula [psi]; `SG`:
    densidade relativa do fluido em relação à água (SG=1 para água). Retorna Q em USGPM — para
    outra convenção de unidades (ex.: Kv em m³/h e bar), a mesma forma da equação vale desde
    que `Cv`/`delta_P` estejam na convenção correspondente. Válida apenas fora de condições de
    escoamento crítico (cavitação em líquidos, choked flow em gases), onde ΔP deixa de ser a
    força motriz efetiva."""
    return Cv * (delta_P / densidade_relativa) ** 0.5


def cv_necessario(vazao: float, delta_P: float, densidade_relativa: float) -> float:
    """Inversa de `vazao_valvula_controle`: o Cv necessário para escoar uma vazão `vazao` dada
    a queda de pressão disponível — o primeiro passo do dimensionamento de uma válvula de
    controle, base para escolher o tamanho/trim na tabela do fabricante."""
    return vazao / (delta_P / densidade_relativa) ** 0.5


def caracteristica_linear(abertura_relativa: float) -> float:
    """Característica de válvula linear: a fração da vazão máxima (Cv/Cv_max) é igual à fração
    de curso aberto — f(x) = x, com x em [0,1]. Usada quando a queda de pressão na válvula é
    aproximadamente constante ao longo da faixa de operação."""
    return abertura_relativa


def caracteristica_igual_percentagem(abertura_relativa: float, rangeabilidade: float = 50.0) -> float:
    """Característica de válvula igual-percentagem (equal percentage): cada incremento igual de
    curso produz um incremento igual *percentual* na vazão — f(x) = R^(x-1), com x (curso
    relativo) em [0,1] e R a rangeabilidade (razão entre o Cv máximo e o mínimo controlável,
    tipicamente 20-50). Em x=1 (totalmente aberta), f=1 (Cv máximo); é a característica preferida
    quando a queda de pressão na válvula varia bastante com a vazão (ex.: a maior parte da perda
    de carga do sistema é na própria válvula em baixa vazão e migra para a tubulação/equipamento
    em alta vazão), já que compensa esse efeito e mantém a malha de controle com ganho
    aproximadamente constante ao longo do curso."""
    return rangeabilidade ** (abertura_relativa - 1.0)
