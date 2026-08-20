# Especificação de Equipamentos

A especificação de um equipamento (datasheet) é o documento que consolida os resultados de
dimensionamento (várias fórmulas já cobertas neste pacote — perda de carga, transferência de
calor, dimensionamento de válvulas, Ergun para leito fixo) nas condições de projeto que o
fabricante precisa para cotar e construir o equipamento. Não é uma fórmula isolada, mas sim o
formato padronizado que une esses cálculos aos requisitos de material, código de projeto aplicável
e condições operacionais.

## O que tipicamente entra em um datasheet

- **Condições de processo**: vazão (normal e de projeto — geralmente com uma margem, ex.: 10-20%
  acima da normal), temperatura, pressão (operação e projeto), composição do fluido.
- **Dimensionamento**: a saída das fórmulas deste pacote — área de troca térmica
  (`transferencia_calor.area_troca_termica`), Cv da válvula (`valvulas_controle.cv_necessario`),
  espessura de parede (`piping.espessura_minima_parede`), etc.
- **Materiais de construção**: escolhidos por compatibilidade química, temperatura e (quando
  relevante) resistência à corrosão — ver Área 10, `engenharia_corrosao.md`.
- **Código de projeto aplicável**: ASME (vasos de pressão — Seção VIII; tubulação — B31.3),
  TEMA (trocadores casco-tubo), API (equipamentos de petróleo/petroquímica) — cada um define
  margens de segurança e métodos de cálculo próprios que podem diferir das fórmulas simplificadas
  deste pacote (ex.: a espessura de parede de vaso de pressão real segue ASME VIII, não só a
  fórmula de Barlow usada aqui para tubulação).

## Por que isso não é redutível a uma função

Um datasheet é fundamentalmente um documento de especificação e comunicação entre o processo (que
define as condições de operação) e a engenharia mecânica/fabricante (que projeta e constrói o
equipamento para essas condições, com suas próprias margens e códigos) — o valor está em reunir e
formatar as informações corretas, não em um cálculo adicional além dos já cobertos pelos outros
módulos deste pacote.
