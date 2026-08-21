"""Integração de processos (Pinch Technology): o Problem Table Algorithm (Linnhoff, 1979) para
determinar as necessidades mínimas de utilidade quente e fria de uma rede de trocadores de calor
— dado um conjunto de correntes que precisam ser aquecidas ou resfriadas, encontra a meta
termodinâmica de energia externa mínima e o ponto de pinch, o "gargalo" térmico que separa a
rede em uma região que só precisa de resfriamento (acima do pinch) e uma que só precisa de
aquecimento (abaixo dele) — a base de todo projeto de recuperação de calor entre processos.

Correntes são especificadas como `(T_suprimento, T_alvo, CP)`: `CP` é a vazão de capacidade
térmica [potência/temperatura, ex. kW/K] — o produto da vazão mássica pelo calor específico —
constante ao longo da corrente (aproximação usual sem mudança de fase); o sentido
suprimento→alvo (esfria ou aquece) é inferido automaticamente, não precisa ser informado à parte.
"""

Corrente = tuple[float, float, float]


def _correntes_deslocadas(correntes_quentes: list[Corrente], correntes_frias: list[Corrente],
                           delta_t_min: float) -> tuple[list[Corrente], list[Corrente]]:
    # Desloca correntes quentes para baixo e frias para cima em delta_t_min/2 cada — o truque do
    # Problem Table Algorithm que reduz a restrição de aproximação mínima de temperatura (ΔTmin
    # entre uma corrente quente e uma fria) a uma simples restrição de não-cruzamento na escala
    # de temperatura deslocada, permitindo tratar quentes e frias na mesma tabela.
    quentes = [(Ts - delta_t_min / 2, Tt - delta_t_min / 2, CP) for Ts, Tt, CP in correntes_quentes]
    frias = [(Ts + delta_t_min / 2, Tt + delta_t_min / 2, CP) for Ts, Tt, CP in correntes_frias]
    return quentes, frias


def tabela_problema_pinch(correntes_quentes: list[Corrente], correntes_frias: list[Corrente],
                           delta_t_min: float) -> dict:
    """Executa o Problem Table Algorithm completo e retorna um dict com:

    - `utilidade_quente_minima`, `utilidade_fria_minima`: as metas de energia externa mínima
      (mesma unidade de potência de CP·ΔT) — o resultado central da análise de pinch.
    - `temperatura_pinch_quente`, `temperatura_pinch_fria`: as temperaturas do ponto de pinch na
      escala real de cada lado (a diferença entre as duas é sempre `delta_t_min`).
    - `cascata_viavel`: a cascata de calor em cada fronteira de intervalo de temperatura, já com
      a utilidade quente mínima somada — todos os valores são >= 0 (a condição de viabilidade
      termodinâmica), com o pinch marcado pelo(s) ponto(s) onde a cascata toca zero.

    O acima do pinch (temperaturas maiores que o pinch) é, estruturalmente, um sistema que só
    precisa de energia externa quente; abaixo do pinch, só de energia externa fria — trocar calor
    entre as duas regiões (através do pinch) sempre aumenta o consumo total de utilidade acima do
    mínimo teórico, a regra de ouro do projeto de redes de trocadores por integração de
    processos."""
    quentes, frias = _correntes_deslocadas(correntes_quentes, correntes_frias, delta_t_min)

    temperaturas = sorted({t for Ts, Tt, _ in quentes + frias for t in (Ts, Tt)}, reverse=True)

    calor_por_intervalo = []
    for i in range(len(temperaturas) - 1):
        T_alto, T_baixo = temperaturas[i], temperaturas[i + 1]
        cp_liquido = 0.0
        for Ts, Tt, CP in quentes:
            lo, hi = min(Ts, Tt), max(Ts, Tt)
            if lo <= T_baixo and hi >= T_alto:
                cp_liquido += CP
        for Ts, Tt, CP in frias:
            lo, hi = min(Ts, Tt), max(Ts, Tt)
            if lo <= T_baixo and hi >= T_alto:
                cp_liquido -= CP
        calor_por_intervalo.append(cp_liquido * (T_alto - T_baixo))

    cascata = [0.0]
    for calor in calor_por_intervalo:
        cascata.append(cascata[-1] + calor)

    utilidade_quente_minima = max(0.0, -min(cascata))
    cascata_viavel = [c + utilidade_quente_minima for c in cascata]
    utilidade_fria_minima = cascata_viavel[-1]
    indice_pinch = cascata_viavel.index(min(cascata_viavel))
    temp_pinch_deslocada = temperaturas[indice_pinch]

    return {
        "utilidade_quente_minima": utilidade_quente_minima,
        "utilidade_fria_minima": utilidade_fria_minima,
        "temperatura_pinch_quente": temp_pinch_deslocada + delta_t_min / 2,
        "temperatura_pinch_fria": temp_pinch_deslocada - delta_t_min / 2,
        "cascata_viavel": cascata_viavel,
    }
