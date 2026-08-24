# PHASE 04, Crons

## Entrada

Use esta fase quando a skill operacional funciona e o SQLite passa em `verify`.

## Objetivo

Criar duas rotinas autônomas: relatório HTML semanal e cobrança diária de gastos às 20h.

## Arquivos do repo a ler

1. `PROCESS.yaml`
2. `prompts/05-prompt-cron-html-e-cobranca.md`
3. `skills/assistente-financeiro-runtime/SKILL.md`

## Procedimento

1. Leia `prompts/05-prompt-cron-html-e-cobranca.md`.
2. Crie cron semanal para relatório HTML.
   Critério: retornar `job_id` ou erro verificável.
3. Crie cron diário às 20h para perguntar se houve gasto no dia.
   Critério: retornar `job_id` ou erro verificável.
4. Liste os crons depois da criação.
   Critério: IDs aparecem na listagem.
5. Rode teste seguro quando possível.
   Critério: relatório gera caminho HTML, cobrança não registra gasto sem resposta.
6. Atualize `finance_assistant_progress.json`.

## Gate de saída

Só avance para `05_experimentacao` quando:

- cron semanal tem ID ou bloqueio do scheduler registrado;
- cron diário tem ID ou bloqueio do scheduler registrado;
- estado dos crons foi lido de volta;
- SQLite continua íntegro.

## Se falhar

Não diga que a automação está pronta. Informe qual cron falhou, o erro e uma próxima ação.
