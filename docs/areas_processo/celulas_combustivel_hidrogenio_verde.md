# Células de Combustível e Hidrogênio Verde

Uma célula de combustível converte energia química diretamente em eletricidade por reação
eletroquímica (H2 + ½O2 → H2O, para uma célula de hidrogênio), sem passar por combustão — o
inverso da eletrólise já coberta em `eletroquimica.py` (que consome eletricidade para produzir
H2 a partir de água). O potencial reversível de uma célula de combustível e a eficiência de um
eletrolisador seguem a mesma base termodinâmica (equação de Nernst,
`eletroquimica.potencial_nernst`) — a diferença está na direção da reação e de onde a energia
entra/sai do sistema.

## Hidrogênio "verde", "azul", "cinza" — a nomenclatura por rota de produção

- **Cinza**: H2 produzido por reforma a vapor de gás natural (a rota dominante hoje,
  intensiva em CO2 — sem captura).
- **Azul**: mesma rota (reforma a vapor), mas com captura e armazenamento do CO2 gerado
  (`captura_carbono_ccs.py`) — reduz, mas não elimina, a pegada de carbono.
- **Verde**: H2 produzido por eletrólise da água usando eletricidade de fontes renováveis — zero
  emissão direta na produção, mas a eficiência energética do processo (eletricidade → H2 →
  eletricidade de volta, se usado em célula de combustível) importa muito para o caso de negócio,
  já que cada conversão perde energia.

## Por que a eficiência de ida-e-volta (round-trip) limita o uso de H2 como armazenamento de energia

Usar hidrogênio verde para armazenar energia renovável intermitente (eletrólise → armazenamento
→ célula de combustível de volta a eletricidade) envolve duas conversões com perdas — a
eficiência de um eletrolisador PEM típico é ~60-80%, e a de uma célula de combustível de volta a
eletricidade também ~50-60%, resultando em uma eficiência de ida-e-volta tipicamente na faixa de
30-45%. Isso torna H2 mais competitivo para armazenamento de longa duração/grande escala (onde
baterias são inviáveis) e para usos que não são eletricidade (matéria-prima química, redução de
minério de ferro, combustível para transporte pesado) do que para armazenamento de energia de
curto prazo, onde baterias com eficiência de ida-e-volta >90% competem diretamente.
