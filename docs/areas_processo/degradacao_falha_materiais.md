# Degradação e Falha de Materiais

Cobre os mecanismos de degradação de materiais em serviço — fadiga, fluência (creep), corrosão
(`engenharia_corrosao.py`), fragilização por hidrogênio, degradação térmica de polímeros — e como
cada um limita a vida útil de um equipamento. É uma disciplina de ciência dos materiais aplicada,
não redutível a uma fórmula única porque cada mecanismo de falha tem sua própria física; mas o
mecanismo de degradação térmica tem uma conexão direta com um conceito já usado neste
repositório.

## Degradação térmica e a lei de Arrhenius

Muitos mecanismos de degradação de materiais (envelhecimento de polímeros, degradação de
isolamento elétrico, desativação de catalisadores por sinterização térmica) seguem cinética tipo
Arrhenius — a mesma relação usada para a cinética de reação em `termodinamica.
constante_velocidade_arrhenius` e no `reator_digital_twin`: a taxa de degradação cresce
exponencialmente com a temperatura. Isso é a base dos testes acelerados de envelhecimento (ex.:
regra empírica de que a vida útil de um isolamento elétrico cai pela metade a cada ~10°C de
aumento de temperatura de operação sustentada — uma aproximação prática da relação de Arrhenius
para esse tipo específico de degradação) — testar o material em temperatura elevada por um tempo
curto, e extrapolar para a vida útil esperada na temperatura de operação real via essa mesma lei.

## Modos de falha mecânica (fora do escopo de fórmula fechada deste repositório)

- **Fadiga**: falha sob carga cíclica, mesmo abaixo do limite de resistência estático — relevante
  para vasos de pressão e tubulações sujeitos a ciclos térmicos/de pressão repetidos (ex.: um
  reator batelada com muitos ciclos de aquecimento/resfriamento).
- **Fluência (creep)**: deformação lenta e contínua sob carga constante em alta temperatura —
  relevante para equipamento operando perto do limite superior de temperatura do material (fornos,
  reatores de alta temperatura).
- **Fragilização por hidrogênio**: hidrogênio atômico penetrando na estrutura do aço em ambientes
  específicos (H2S úmido — "sour service", comum em refino), reduzindo a ductilidade e podendo
  causar falha frágil repentina.

## Por que isso conecta com gestão de ativos e RCM

A seleção de qual mecanismo de degradação monitorar (e como) para um equipamento específico é
exatamente a pergunta central de `manutencao_centrada_confiabilidade_mcc.md` (Área 8) — cada modo
de falha de material tem sua própria técnica de monitoramento apropriada (análise de vibração para
fadiga incipiente, medição de espessura por ultrassom para corrosão/fluência, réplicas metalográficas
para dano por fluência acumulado).
