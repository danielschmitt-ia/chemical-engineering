"""Adsorção e troca iônica: isotermas de equilíbrio de Langmuir e Freundlich, e uma estimativa
estequiométrica ideal (limite superior) do tempo de ruptura de um leito adsorvedor.
"""


def isoterma_langmuir(C: float, q_max: float, K: float) -> float:
    """Isoterma de Langmuir (adsorção em monocamada, sítios idênticos e independentes):
    q = q_max·K·C/(1+K·C). `C`: concentração do soluto em equilíbrio na fase fluida; `q_max`:
    capacidade máxima de adsorção (monocamada saturada); `K`: constante de equilíbrio de
    Langmuir. Para K·C << 1 (baixa concentração), q ≈ q_max·K·C (linear); para K·C >> 1
    (alta concentração), q → q_max (saturação)."""
    return q_max * K * C / (1.0 + K * C)


def isoterma_freundlich(C: float, Kf: float, n: float) -> float:
    """Isoterma de Freundlich (empírica, para superfícies heterogêneas): q = Kf·C^(1/n). `n`
    tipicamente > 1 (n=1 recupera adsorção linear/Henry); ao contrário de Langmuir, não prevê um
    platô de saturação — só é fisicamente razoável dentro da faixa de concentração em que foi
    ajustada."""
    return Kf * C ** (1.0 / n)


def tempo_ruptura_estequiometrico(massa_adsorvente: float, capacidade_adsorcao: float,
                                   vazao_massica_soluto: float) -> float:
    """Estimativa estequiométrica (ideal) do tempo até a ruptura (breakthrough) de um leito
    adsorvedor: tempo até que toda a capacidade do leito seja consumida, assumindo utilização
    100% da capacidade e uma frente de adsorção infinitamente estreita —

        t_ruptura = massa_adsorvente·capacidade_adsorção / vazão_mássica_soluto

    Um LIMITE SUPERIOR otimista: ignora a zona de transferência de massa (a frente de adsorção
    real tem espessura finita, e o leito "rompe" antes de toda sua capacidade ser usada) — útil
    como estimativa inicial de ordem de grandeza, não para dimensionamento final. `capacidade_
    adsorcao` na mesma base de massa de soluto por massa de adsorvente que definiu q_max/Kf nas
    isotermas acima."""
    return massa_adsorvente * capacidade_adsorcao / vazao_massica_soluto
