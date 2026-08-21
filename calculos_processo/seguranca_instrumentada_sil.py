"""Sistemas instrumentados de segurança (SIS) e parada de emergência (ESD): a métrica central de
desempenho de uma função instrumentada de segurança (SIF) sob a norma IEC 61508/61511 — a
probabilidade média de falha em demanda (PFDavg) — e a classificação em Nível de Integridade de
Segurança (SIL) que ela determina. O SIS conceitual já implementado e testado em
`reator_digital_twin/modelo.py` (`_avancar_com_sis`, `simular_interlock_seguranca`) é o exemplo
concreto deste repositório de uma função de proteção independente — ver
`docs/areas_processo/sis_intertravamento_seguranca.md`.
"""

_FAIXAS_SIL = (
    (1e-5, 1e-4, 4),
    (1e-4, 1e-3, 3),
    (1e-3, 1e-2, 2),
    (1e-2, 1e-1, 1),
)


def pfd_media_1oo1(taxa_falha_perigosa_nao_detectada: float, intervalo_teste_prova: float) -> float:
    """Probabilidade média de falha em demanda (PFDavg) de uma arquitetura simples 1oo1 (um
    único canal, sem redundância, sem diagnóstico automático), com teste de prova periódico —
    a aproximação simplificada padrão da IEC 61508/ISA-TR84 (válida quando λ·TI << 1, o caso
    usual):

        PFDavg ≈ λ_DU · TI / 2

    `taxa_falha_perigosa_nao_detectada` (λ_DU): taxa de falhas perigosas não detectadas [1/tempo];
    `intervalo_teste_prova` (TI): intervalo entre testes de prova periódicos, na mesma unidade de
    tempo de λ_DU. O fator 1/2 vem da falha, em média, ocorrer na metade do intervalo entre
    testes — metade do tempo a função de segurança já falhou silenciosamente sem que ninguém
    saiba, até o próximo teste de prova revelar."""
    return taxa_falha_perigosa_nao_detectada * intervalo_teste_prova / 2.0


def nivel_sil_a_partir_de_pfd(pfd_avg: float) -> int:
    """Nível de Integridade de Segurança (SIL) correspondente a um PFDavg, pelas faixas da
    IEC 61508 (modo de operação de baixa demanda — a demanda na função de segurança ocorre com
    menos frequência que uma vez por ano):

        SIL 4: 1e-5 <= PFDavg < 1e-4
        SIL 3: 1e-4 <= PFDavg < 1e-3
        SIL 2: 1e-3 <= PFDavg < 1e-2
        SIL 1: 1e-2 <= PFDavg < 1e-1

    Levanta `ValueError` se `pfd_avg` estiver fora da faixa SIL 1-4 (PFDavg >= 0.1 não atinge
    nem o SIL mais baixo; PFDavg < 1e-5 excede o que a IEC 61508 cobre com uma única função — na
    prática, exigiria arquitetura redundante com múltiplas camadas independentes)."""
    for limite_inferior, limite_superior, sil in _FAIXAS_SIL:
        if limite_inferior <= pfd_avg < limite_superior:
            return sil
    raise ValueError(f"PFDavg={pfd_avg} fora da faixa SIL 1-4 (1e-5 a 1e-1)")
