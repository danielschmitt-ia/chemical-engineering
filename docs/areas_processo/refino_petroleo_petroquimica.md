# Refino de Petróleo e Petroquímica

Refino de petróleo é, historicamente, a indústria onde a maioria das operações unitárias deste
pacote foi desenvolvida e refinada — destilação (`destilacao.py`, embora o refino real trabalhe
com misturas multicomponentes complexas, não o binário deste pacote), craqueamento catalítico
(`reatores_leito_fixo.py`/`fluidizacao.py` — o craqueamento catalítico fluido, FCC, é o exemplo
histórico mais citado de reator de leito fluidizado circulante, item 2.5 deste roteiro),
hidrotratamento (leito fixo catalítico) e as utilidades de larga escala que sustentam essas
unidades (`geracao_vapor.py`, `refrigeracao.py`). Petroquímica é a extensão dessa base para
produzir monômeros e intermediários químicos (eteno, propeno, benzeno) a partir de frações de
petróleo, alimentando as rotas de síntese de plásticos e outros produtos químicos.

## Por que o controle avançado (APC/MPC) é padrão de mercado nessa indústria

O `README.md` principal já cita isso na seção de aplicações industriais: "Refino e petroquímica
de base: controle preditivo multivariável (APC/MPC) já é padrão de mercado em unidades de reação,
com restrições de segurança embutidas no otimizador" — exatamente o tipo de MPC que o
`reator_digital_twin` implementa, e a razão histórica é a escala: uma unidade de craqueamento ou
destilação de refino processa dezenas de milhares de barris por dia, então mesmo um ganho pequeno
de eficiência energética ou de rendimento (o tipo de otimização que o Economic MPC deste
repositório ilustra) se traduz em valor absoluto muito grande — justificando o investimento em
controle avançado que uma unidade menor talvez não justificasse.

## A cadeia de valor: do petróleo bruto aos produtos petroquímicos

1. **Destilação atmosférica e a vácuo**: separação inicial do petróleo bruto em frações por faixa
   de ebulição (nafta, querosene, diesel, resíduo) — destilação multicomponente em grande escala.
2. **Conversão**: craqueamento (térmico ou catalítico — FCC) quebra moléculas grandes em menores
   e mais valiosas; reforma catalítica aumenta a octanagem da nafta.
3. **Tratamento**: hidrotratamento remove enxofre e outros contaminantes (leito fixo catalítico,
   `reatores_leito_fixo.py`), atendendo especificações de combustível cada vez mais restritivas.
4. **Petroquímica**: eteno e propeno (da unidade de craqueamento a vapor de nafta/etano) e
   aromáticos (benzeno, tolueno, xileno, da reforma catalítica) alimentam as rotas de síntese de
   polímeros (`engenharia_polimeros.py`) e outros intermediários químicos.
