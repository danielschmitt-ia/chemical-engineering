# Avaliação do Ciclo de Vida (ACV / LCA)

ACV (Life Cycle Assessment, normatizada pela ISO 14040/14044) quantifica os impactos ambientais
de um produto ou processo ao longo de todo seu ciclo de vida — da extração de matéria-prima
("berço") até o descarte final ou reciclagem ("túmulo", ou "berço-ao-berço" quando o material
retorna ao ciclo produtivo) — não só a etapa de manufatura isolada. Não é redutível a uma única
fórmula porque agrega múltiplas categorias de impacto (mudança climática, acidificação,
eutrofização, toxicidade humana, uso de água — ver `metricas_hidricas.py`, uso de recursos)
através de fatores de caracterização específicos de cada categoria, definidos por metodologias
padronizadas (ex.: ReCiPe, TRACI, CML), não uma fórmula fechada única.

## As quatro fases de uma ACV (ISO 14040)

1. **Definição de objetivo e escopo**: o que está sendo comparado, a unidade funcional (a base
   de comparação — ex.: "1 kg de produto entregue ao cliente", não só "1 kg saindo da fábrica",
   para incluir embalagem/transporte se relevante ao escopo) e os limites do sistema.
2. **Inventário do ciclo de vida (ICV/LCI)**: quantificação de todas as entradas (matéria-prima,
   energia, água) e saídas (emissões, resíduos) em cada etapa — os balanços de massa e energia
   deste pacote (`balanco_massa.py`, `balanco_energia.py`, `balanco_carbono.py`) são exatamente o
   tipo de dado que alimenta essa fase.
3. **Avaliação de impacto (AICV/LCIA)**: os fluxos do inventário são convertidos em impactos por
   categoria via fatores de caracterização (ex.: kg CO2-equivalente por kg de metano emitido, o
   fator de potencial de aquecimento global do metano) — cada categoria de impacto tem sua
   metodologia própria de agregação.
4. **Interpretação**: identificação dos processos/etapas que mais contribuem para cada impacto
   (hotspots), e análise de sensibilidade/incerteza dos resultados.

## Por que a unidade funcional é a decisão mais importante de uma ACV

Comparar dois processos por "impacto por kg produzido" pode inverter completamente o resultado
frente a "impacto por unidade de serviço entregue" se os processos tiverem eficiências,
durabilidades ou desempenhos por unidade diferentes — a escolha errada da unidade funcional é a
fonte mais comum de uma ACV que chega a uma conclusão enganosa, mesmo com dados de inventário
tecnicamente corretos.
