# Tratamento de Gases de Exaustão

Tratamento de gases de exaustão (ex.: dessulfurização de gases de combustão/FGD, redução
catalítica seletiva de NOx, lavadores de particulados) usa, no núcleo, a mesma matemática de
absorção gás-líquido já implementada em `absorcao_stripping.py` (fator de absorção, equação de
Kremser para o número de estágios) — a diferença frente a uma absorvedora de processo convencional
é o objetivo (remover um poluente até um limite regulatório, não recuperar um produto de valor) e
as reações químicas específicas envolvidas na captura.

## As tecnologias mais comuns, e onde cada módulo deste pacote se aplica

- **Dessulfurização (FGD, ex.: lavador úmido com calcário)**: absorção de SO2 em uma suspensão
  aquosa de calcário, com reação química (SO2 + CaCO3 + ½O2 → CaSO4 + CO2) — o dimensionamento do
  lavador segue `absorcao_stripping.py` (fator de absorção, estágios), com a taxa de reação
  adicionando um termo de intensificação frente à absorção física pura.
- **Redução catalítica seletiva (SCR) de NOx**: injeção de amônia sobre um catalisador para
  reduzir NOx a N2 e água — mais próxima da cinética de `reatores_leito_fixo.py` (leito fixo
  catalítico, efetividade via módulo de Thiele) que de absorção.
- **Filtração de particulados** (filtro de manga, precipitador eletrostático): remoção física de
  material particulado — mais próxima de `filtragem.py` (embora a filtração de gases use
  princípios de captura de partículas por impactação/difusão distintos da filtração em torta
  líquida modelada ali).
- **Captura de CO2** (`captura_carbono_ccs.py`): tipicamente por absorção química com aminas —
  novamente a mesma base de `absorcao_stripping.py`.

## A métrica comum: eficiência de remoção

Independente da tecnologia, o desempenho é reportado da mesma forma que qualquer outra etapa de
tratamento ambiental — `tratamento_efluentes.eficiencia_remocao` (a mesma fórmula, aplicada à
concentração do poluente na corrente gasosa em vez de líquida) — comparado contra o limite de
emissão outorgado na licença ambiental (`licenciamento_ambiental.md`) para aquele poluente
específico.
