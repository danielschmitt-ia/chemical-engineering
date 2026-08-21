# Layout de Planta Industrial

Layout de planta é a disposição física de equipamentos, tubulações, vias de acesso e edificações
no terreno — dirigida por distâncias mínimas de segurança normatizadas (não uma fórmula fechada,
mas valores tabelados por norma), fluxo de processo eficiente, e acesso para operação, manutenção
e resposta a emergência.

## Distâncias de referência (ordem de grandeza — a norma aplicável e a análise de risco específica
do projeto sempre prevalecem sobre estes valores)

| Entre | Distância típica de referência |
|---|---|
| Vaso de processo com inventário inflamável e a cerca do limite de bateria | Dezenas de metros (tipicamente 15-30 m), conforme API RP 752/753 e a análise de risco do site |
| Área de processo e sala de controle não classificada como área explosiva | Distância suficiente para resistir a sobrepressão de uma explosão de nuvem de vapor crível — dimensionada por análise de risco (blast resistant design), não uma tabela fixa universal |
| Tanques de armazenamento de inflamáveis entre si | Definida pela NFPA 30 em função do diâmetro do tanque e do tipo de líquido armazenado |
| Equipamento rotativo (bombas, compressores) e via de acesso para manutenção | Espaço para remoção do rotor/acesso de guindaste, tipicamente 1-1.5x o comprimento do equipamento |

Esses números são pontos de partida de ordem de grandeza — o dimensionamento real de layout de
uma planta com inventário de material perigoso segue uma análise de consequência (dispersão de
gás tóxico, radiação térmica de incêndio, sobrepressão de explosão) específica do site, não uma
fórmula genérica.

## Por que layout é uma disciplina de segurança, não só de conveniência operacional

Os acidentes reais citados no `README.md` principal deste repositório (T2 Laboratories, Synthron)
envolveram perda de contenção com liberação de energia — o layout é a última linha de defesa
física quando as camadas de proteção do processo (MPC, SIS — ver `mpc_controle_preditivo.md` e
Área 8, `sis_intertravamento_seguranca.md`) falham: a distância entre um vaso de risco e
áreas ocupadas determina literalmente quantas pessoas estão na zona de consequência se o pior
cenário crível (o mesmo tipo de cenário que `reator_digital_twin.simular_runaway` avalia para o
reator deste repositório) se concretizar.
