# PHASE 01, Misamplace

## Entrada

Use esta fase quando o aluno começou o processo pelo link do repositório e ainda não existe SQLite financeiro confiável.

## Regra de condução

Faça uma pergunta por vez. Não peça anexos do processo. Busque prompts, templates e instruções no repositório. Peça ao aluno somente dados pessoais financeiros que não podem existir no GitHub público.

## Arquivos do repo a ler

1. `WEB_BOOTSTRAP.md`
2. `PROCESS_MANIFEST.json`
3. `PROCESS.yaml`
4. `CHECKPOINT_SCHEMA.json`
5. `prompts/01-systemprompt-entrevista-misamplace.md`
6. Templates em `misamplace-template/`

## Checklist de coleta

Coletar ou registrar lacuna para:

- nome e forma de tratamento;
- separação PF e PJ;
- saldos atuais em bancos PF;
- saldos atuais em bancos PJ;
- cartões PF;
- cartões PJ;
- dia de fechamento e vencimento de cada cartão;
- empréstimos pendentes;
- receitas;
- despesas recorrentes;
- faturas atuais;
- gastos recentes ainda não postados.

## Perguntas recomendadas

Comece com:

```text
Vamos montar seu Misamplace financeiro. Primeiro: quais contas bancárias você usa hoje, separando PF e PJ, e qual o saldo aproximado de cada uma?
```

Depois siga uma pergunta por vez, priorizando o gate pendente.

## Atualização do checkpoint

Depois de cada resposta útil, atualize `finance_assistant_progress.json`:

- `current_state`: `01_misamplace`
- `pending_gates`: gate ainda faltante;
- `open_gaps`: lacunas explícitas;
- `last_user_message_summary`;
- `last_assistant_action_summary`.

## Gate de saída

Só avance para `02_preparo` quando:

- PF/PJ foram identificados ou lacuna registrada;
- pelo menos uma conta ou cartão foi registrado, ou ausência de ambos foi registrada como lacuna;
- datas de fechamento e vencimento foram pedidas para cada cartão conhecido;
- lacunas abertas foram listadas;
- o aluno confirmou que pode seguir para criar o banco inicial.

## Se falhar

Não avance. Faça uma única pergunta concreta ou peça um único documento pessoal específico.
