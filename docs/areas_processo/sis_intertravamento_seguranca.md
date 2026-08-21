# Sistemas de Parada de Emergência (ESD) e de Intertravamento de Segurança (SIS)

Não é um novo módulo de simulação porque este repositório já implementa e testa um SIS
conceitual completo: `reator_digital_twin/modelo.py` (`_avancar_com_sis`,
`simular_interlock_seguranca`) — um trip *hard-wired*, independente do modelo do MPC, que força
resfriamento máximo quando a temperatura medida cruza `T_trip_sis`, contendo um cenário de
descasamento de modelo que o MPC sozinho não conteria (ver a seção "Camada de Proteção
Independente (SIS)" do `README.md` principal). Os cálculos quantitativos de PFDavg e nível SIL
que dimensionam um SIS real ficam em `calculos_processo/seguranca_instrumentada_sil.py`.

## ESD vs. SIS — a relação entre os dois termos

Um ESD (Emergency Shutdown System) é, na prática, um caso específico de SIS: um sistema
instrumentado de segurança cuja ação é levar o processo (ou toda a planta) a um estado seguro por
parada, em vez de uma ação mais localizada (ex.: um trip de temperatura em um único reator, como
o deste repositório). A norma (IEC 61511) trata ambos sob o mesmo arcabouço — SIF (Safety
Instrumented Function), com seu próprio SIL — o ESD é tipicamente a SIF de maior abrangência e
maior consequência de uma planta, frequentemente com múltiplos níveis (ESD parcial de uma unidade
vs. ESD total do site).

## Por que o SIS deste repositório é conceitual, não certificado

Ver `docs/PROJETO_INDUSTRIAL.md` para o tratamento completo — em resumo, um SIS real certificado
IEC 61508/61511 exige: hardware com dados de falha (SFF, HFT) para a arquitetura escolhida,
lógica solver certificado (não um laço de simulação Python), sensores/atuadores com certificado
próprio, e um ciclo de vida de segurança completo (verificação independente, teste de prova
documentado, gestão de mudanças específica para a SIF). O `_avancar_com_sis` deste repositório
demonstra a *lógica* (trip independente do modelo de controle, ação pré-definida) — não substitui
esse ciclo de vida para uma aplicação real.

## Onde o PFDavg entra

`seguranca_instrumentada_sil.pfd_media_1oo1` calcula a probabilidade média de falha em demanda de
uma arquitetura simples de canal único — a métrica que, comparada às faixas de
`nivel_sil_a_partir_de_pfd`, determina se um SIS proposto atinge o SIL alvo definido pela LOPA
(`seguranca_processo_industrial.md`) para aquele cenário específico.
