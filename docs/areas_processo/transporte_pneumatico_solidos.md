# Transporte Pneumático de Sólidos

Transporte de partículas sólidas suspensas em um fluxo de gás (normalmente ar) através de
tubulação. Ao contrário dos demais itens da área "Fundamentos e Fenômenos de Transporte" deste
repositório, não é tratado como módulo de código em `calculos_processo/`: as correlações de
projeto (velocidade mínima de transporte, queda de pressão bifásica) são fortemente empíricas,
específicas do material particulado (tamanho, forma, densidade, coesão) e divergem
significativamente entre fontes — codificar uma delas sem validação experimental para o material
real seria apresentar uma falsa precisão. Esta nota resume os conceitos e aponta a literatura de
referência para quando o dimensionamento real for necessário.

## Regimes de escoamento

- **Fase diluída** (baixa razão de carga de sólidos, alta velocidade de gás): partículas
  suspensas individualmente, arrasto domina — regime mais previsível e mais usado quando a
  natureza do produto permite.
- **Fase densa** (alta razão de carga, baixa velocidade): sólidos se movem em êmbolos, dunas ou
  leito deslizante no fundo do tubo — menor consumo de energia por tonelada transportada, mas
  exige equipamento de alimentação mais elaborado (vasos de pressão tipo *blow tank*) e é mais
  sensível às propriedades do material.

## Parâmetros-chave de projeto

- **Razão de carga de sólidos** (`ṁ_sólido / ṁ_gás`): o parâmetro central que separa fase diluída
  de fase densa; tipicamente < 15 para diluída, podendo passar de 100 em fase densa.
- **Velocidade de transporte**: precisa ficar acima da velocidade de saltação (limite abaixo do
  qual as partículas começam a se depositar no fundo do tubo, em transporte horizontal) com uma
  margem de segurança — operar perto demais do limite arrisca entupimento; longe demais desperdiça
  energia e aumenta erosão/atrito nas curvas.
- **Velocidade terminal da partícula** (ver `calculos_processo.mecanica_fluidos.velocidade_terminal_stokes`
  para partículas finas em regime de Stokes) informa a ordem de grandeza mínima de velocidade de
  gás necessária, mas não substitui uma correlação de saltação específica do material.
- **Queda de pressão total**: soma da perda do gás puro (`calculos_processo.perda_carga`) com a
  perda adicional devido à presença dos sólidos (aceleração das partículas, atrito
  partícula-parede, elevação) — esta última é a parcela dominada pelas correlações empíricas
  específicas do material.

## Quando aprofundar

Para um projeto real, a prática usual é: (1) caracterizar o material (distribuição
granulométrica, densidade, ângulo de repouso, abrasividade), (2) rodar testes de bancada ou usar
dados de um fornecedor de sistema pneumático para obter a velocidade mínima de transporte e o
fator de correlação de queda de pressão específicos daquele material, e (3) dimensionar com
margem de segurança sobre esses valores medidos — referências de projeto amplamente usadas na
indústria incluem Mills, *Pneumatic Conveying Design Guide*, e Klinzing et al., *Pneumatic
Conveying of Solids*.
