"""Fração molar de misturas: conversão entre base mássica e molar, massa molar média de uma
mistura e pressão parcial (lei de Dalton) — as conversões de composição usadas como entrada
pelos demais módulos de cálculo de processo (destilação, balanço de massa por componente)."""

from collections.abc import Mapping


def _validar_soma_um(fracoes: Mapping[str, float], tol: float = 1e-6) -> None:
    soma = sum(fracoes.values())
    if abs(soma - 1.0) > tol:
        raise ValueError(f"Frações devem somar 1, somaram {soma}")


def massa_molar_media(fracoes_molares: Mapping[str, float], massas_molares: Mapping[str, float]) -> float:
    """Massa molar média de uma mistura: M̄ = Σ(x_i·M_i), com x_i as frações molares e M_i as
    massas molares de cada componente (mesma unidade de M_i para todos, tipicamente g/mol)."""
    _validar_soma_um(fracoes_molares)
    return sum(fracoes_molares[c] * massas_molares[c] for c in fracoes_molares)


def fracao_molar_a_partir_massica(fracoes_massicas: Mapping[str, float],
                                   massas_molares: Mapping[str, float]) -> dict[str, float]:
    """Converte frações mássicas para frações molares: x_i = (w_i/M_i) / Σ(w_j/M_j) — primeiro
    converte cada componente para uma base proporcional a mols (w_i/M_i), depois normaliza."""
    _validar_soma_um(fracoes_massicas)
    mols_relativos = {c: fracoes_massicas[c] / massas_molares[c] for c in fracoes_massicas}
    total = sum(mols_relativos.values())
    return {c: valor / total for c, valor in mols_relativos.items()}


def fracao_massica_a_partir_molar(fracoes_molares: Mapping[str, float],
                                   massas_molares: Mapping[str, float]) -> dict[str, float]:
    """Converte frações molares para frações mássicas: w_i = (x_i·M_i) / Σ(x_j·M_j)."""
    _validar_soma_um(fracoes_molares)
    massa_relativa = {c: fracoes_molares[c] * massas_molares[c] for c in fracoes_molares}
    total = sum(massa_relativa.values())
    return {c: valor / total for c, valor in massa_relativa.items()}


def pressao_parcial(fracao_molar: float, pressao_total: float) -> float:
    """Pressão parcial de um componente em uma mistura gasosa ideal (lei de Dalton):
    p_i = x_i·P. Mesma unidade de pressão retornada que `pressao_total`."""
    return fracao_molar * pressao_total
