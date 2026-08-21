# Fluxogramas de Engenharia (P&ID)

Um P&ID (Piping and Instrumentation Diagram — não confundir com o controlador PID de
`controle_pid.py`, é uma sigla coincidente) é a representação simbólica padronizada (ISA S5.1)
de todos os equipamentos, tubulações, válvulas, instrumentos e malhas de controle de uma planta —
o documento de engenharia mais detalhado e mais usado no dia a dia de operação, manutenção e
comissionamento. É uma convenção de representação gráfica e simbólica, não um cálculo.

## O que um P&ID mostra (que um PFD não mostra)

Comparado a um PFD (`fluxograma_pfd.md`, mais conceitual), um P&ID inclui todo o detalhe de
implementação real: cada válvula manual e de controle, cada instrumento (com sua tag ISA — ex.
"TIC-101" para um controlador indicador de temperatura, malha 101), linhas de sinal (elétrico,
pneumático, dados), intertravamentos de segurança (o SIS de `reator_digital_twin` seria
representado aqui com sua própria simbologia de malha de segurança), drenos, vents, e a
especificação de linha (diâmetro, material, classe de pressão) de cada trecho de tubulação.

## Simbologia essencial (ISA S5.1)

- **Círculo**: instrumento de campo montado localmente.
- **Círculo com linha horizontal**: instrumento montado em painel/sala de controle, acessível ao
  operador.
- **Letras dentro do círculo**: função (a primeira letra é a variável medida — T=temperatura,
  P=pressão, F=vazão, L=nível, A=análise; as seguintes são a função — I=indicador, C=controlador,
  T=transmissor, A=alarme). Ex.: "PIC" = Pressure Indicating Controller.
- **Linhas de processo**: tubulação (linha contínua grossa); linha de instrumento/sinal (linha
  fina, tracejada para sinal elétrico ou pneumático conforme convenção do projeto).

## Onde isso se conecta com o resto do repositório

O SIS conceitual de `reator_digital_twin` (trip de temperatura, força resfriamento máximo) seria
representado em um P&ID real com a simbologia específica de malha de segurança (tipicamente um
losango dentro do círculo do instrumento, seguindo IEC 61511) — distinta da malha de controle
regulatório normal, justamente para deixar visualmente claro, na planta e para quem opera, que
aquela malha é independente do sistema básico de controle (BPCS).
