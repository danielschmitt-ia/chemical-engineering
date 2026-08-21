# Processamento de Cerâmicas Avançadas

Cerâmicas avançadas (alumina, zircônia, carbeto de silício, nitreto de silício — distintas de
cerâmicas tradicionais como louça e tijolo pela pureza controlada e microestrutura projetada)
usadas em aplicações de alto desempenho (isolamento elétrico, componentes resistentes a desgaste
e alta temperatura, substratos eletrônicos). O processamento compartilha etapas com engenharia de
partículas (`engenharia_particulas.py`) e secagem (`secagem.py`) deste pacote, mais uma etapa
específica — sinterização — fora do escopo de fórmula fechada aqui.

## As etapas típicas

1. **Preparação do pó**: controle rígido de tamanho de partícula e pureza (a distribuição
   granulométrica, caracterizada pelo diâmetro médio de Sauter de `engenharia_particulas.py`,
   controla diretamente a densidade de empacotamento e, por consequência, a densidade final da
   peça sinterizada).
2. **Conformação**: moldagem do pó em verde (compactação uniaxial/isostática, moldagem por
   injeção, colagem de fita) na forma final ou próxima da final.
3. **Secagem**: remoção controlada do solvente/ligante da peça em verde — controlada com cuidado
   maior que a secagem industrial genérica de `secagem.py`, porque uma taxa de secagem rápida
   demais gera gradientes de umidade que trincam a peça antes mesmo da sinterização.
4. **Sinterização**: aquecimento a alta temperatura (tipicamente 50-80% da temperatura de fusão do
   material) para densificar a peça por difusão em estado sólido, eliminando porosidade — a etapa
   que mais determina as propriedades mecânicas finais, e que não tem uma fórmula fechada de uso
   geral (a cinética de densificação depende fortemente do sistema de material específico).

## Por que cerâmicas avançadas são mais sensíveis a defeito que metais

Ao contrário de um metal (que deforma plasticamente antes de fraturar, absorvendo energia), uma
cerâmica é intrinsecamente frágil — um defeito microscópico (poro, trinca, inclusão) que um metal
tolera sem consequência pode ser o ponto de iniciação de fratura catastrófica em uma cerâmica. Por
isso o controle de processo em cada etapa acima (pureza do pó, uniformidade de compactação, taxa
de secagem controlada, perfil de sinterização) é desproporcionalmente mais rígido que em
processamento metalúrgico equivalente — o mesmo princípio de controle estatístico de processo
(`controle_estatistico_processo.py`, Cp/Cpk) aplicado com tolerâncias muito mais apertadas.
