# Manutenção Centrada na Confiabilidade (MCC / RCM)

RCM (Reliability Centered Maintenance) é a metodologia que decide *qual* estratégia de manutenção
(corretiva, preventiva, preditiva — ver `manutencao_preditiva_proativa.md`) aplicar a *cada*
equipamento, com base sistemática na função do equipamento, seus modos de falha prováveis (a
mesma análise de `fmea_rpn.py`) e a consequência de cada falha — em vez de aplicar a mesma
estratégia genérica (ex.: "trocar tudo a cada 6 meses") a toda a planta.

## A pergunta central do RCM, por equipamento

1. **Qual é a função do equipamento** (incluindo os padrões de desempenho esperados)?
2. **De que formas ele pode falhar em cumprir essa função** (modos de falha — a mesma pergunta
   de uma FMEA, `fmea_rpn.py`)?
3. **O que causa cada modo de falha?**
4. **O que acontece quando cada falha ocorre** (consequência — segurança, ambiental, operacional,
   econômica)?
5. **A falha é evidente para a operação, ou oculta** (só descoberta em uma inspeção ou quando a
   função de proteção associada é demandada — o caso clássico de um SIS: uma falha oculta no
   sensor do intertravamento só aparece quando o trip deveria disparar e não dispara)?
6. **O que pode ser feito para prevenir ou detectar cada falha, e vale o custo?**

## Por que isso muda a estratégia (e não é só "mais inspeção")

O RCM frequentemente conclui que a estratégia certa para um componente de baixa consequência de
falha é *nenhuma* manutenção proativa — deixar falhar e trocar (corretiva), porque o custo de
monitorar/trocar preventivamente excede o custo esperado da falha. Ao mesmo tempo, para uma falha
oculta com consequência de segurança (o caso de um componente do SIS), a única estratégia
sensata é teste de prova periódico (o mesmo `intervalo_teste_prova` que entra no cálculo de
PFDavg em `seguranca_instrumentada_sil.py`) — sem ele, a falha oculta pode persistir
indefinidamente sem que ninguém saiba que a camada de proteção já não protege mais.
