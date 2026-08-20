# Comissionamento de Plantas

Comissionamento é a sequência estruturada de verificação, teste e partida de uma planta nova (ou
de uma modificação relevante), progressivamente de sistemas individuais até a operação integrada
— o processo que leva do "construído conforme o projeto" ao "operando de forma segura e
confiável". Não é um cálculo, mas segue uma progressão bem definida que vale registrar, e conecta
diretamente com o roadmap de implantação deste repositório (`docs/PROJETO_INDUSTRIAL.md`, seção
"simulação → shadow mode → piloto → produção" — o comissionamento de um gêmeo digital segue uma
lógica similar de verificação incremental antes de confiar nele em malha fechada real).

## As fases típicas

1. **Verificação estática (pré-comissionamento)**: inspeção visual, testes de continuidade
   elétrica, testes de pressão/estanqueidade em tubulações (hidrostático/pneumático), verificação
   de instalação conforme P&ID e datasheets (`especificacao_equipamentos.md`) — nada energizado
   ou em movimento ainda.
2. **Comissionamento a frio**: energização e teste funcional de instrumentos e malhas de controle
   sem o fluido de processo real (ou com um fluido inerte) — verifica que cada malha (incluindo
   as de segurança, ver `sis_intertravamento_seguranca.md`) responde como projetado antes de
   qualquer risco de processo estar presente.
3. **Comissionamento a quente / partida (start-up)**: introdução do fluido de processo real,
   rampa progressiva até as condições de operação normais, com testes funcionais dos
   intertravamentos de segurança sob condições reais (ou o mais próximo possível) antes de operar
   continuamente.
4. **Testes de performance (performance test run)**: verificação de que a planta atinge as
   garantias de processo contratadas (capacidade, eficiência, especificação de produto) sob
   condições de operação normal sustentada.

## Por que a ordem importa

Cada fase reduz progressivamente a energia/perigo presente antes de introduzir a próxima
variável — testar as malhas de segurança a frio (fase 2) antes de introduzir o fluido de processo
real (fase 3) garante que, quando o processo perigoso de fato começar, as camadas de proteção já
estão verificadas funcionando, não sendo testadas pela primeira vez sob condições reais de risco.
