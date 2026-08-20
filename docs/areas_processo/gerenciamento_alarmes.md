# Gerenciamento de Alarmes

Gestão de alarmes é principalmente uma disciplina de projeto e governança (racionalização de
alarmes, prioridades, supressão de alarmes redundantes durante uma falha maior) normatizada pela
ISA-18.2 / IEC 62682, não um cálculo fechado — mas a norma define métricas quantitativas de
desempenho que valem registrar como referência, já que orientam quando um sistema de alarmes
precisa de racionalização.

## Métricas de referência (ISA-18.2 / EEMUA 191)

| Métrica | Faixa aceitável | Faixa problemática |
|---|---|---|
| Alarmes por hora (operador, média) | < 6 (bom); ~1-2 é considerado "muito bom" | > 12 (sobrecarrega o operador) |
| Alarmes nos primeiros 10 min após um distúrbio maior | < 10 | dezenas a centenas (alarm flood) |
| % do tempo em "alarm flood" (>10 alarmes/10 min) | < 1% | > 1% do tempo operacional |
| Alarmes "crônicos" (mesmo alarme repetindo, geralmente mal ajustado) | 1% dos alarmes configurados gerando > 50% do volume é o padrão típico de planta não racionalizada | — |

Esses números são benchmarks de referência da norma/literatura do setor, não uma fórmula fechada
que se calcula a partir de parâmetros de processo — servem para comparar contra o histórico real
de alarmes de uma planta (extraído do sistema de gerenciamento de alarmes/histórico do DCS) e
decidir se uma campanha de racionalização é necessária.

## Por que isso importa

Um "alarm flood" durante um distúrbio real é exatamente quando o operador mais precisa de clareza
— e é o cenário em que sistemas mal racionalizados falham (o operador não consegue identificar o
alarme causa-raiz em meio a dezenas de alarmes consequentes). A racionalização remove alarmes
redundantes, ajusta prioridades para refletir a urgência real, e usa supressão baseada em estado
(ex.: suprimir alarmes de baixa pressão a jusante quando uma bomba já está com um alarme de
parada) para reduzir o ruído sem esconder informação relevante.
