# PHASE 03, Operação

## Entrada

Use esta fase quando o SQLite inicial existe e `verify` passou.

## Objetivo

Instalar a skill operacional, confirmar leitura do banco e preparar o assistente para registrar gastos reais.

## Arquivos do repo a ler

1. `PROCESS.yaml`
2. `skills/assistente-financeiro-runtime/SKILL.md`
3. `skills/assistente-financeiro-runtime/scripts/finance_db.py`
4. `skills/assistente-financeiro-runtime/scripts/generate_weekly_html.py`
5. `scripts/install_skills.py`

## Procedimento

1. Instale ou copie a skill `assistente-financeiro-runtime` para o profile ativo.
   Critério: diretório da skill existe no profile ou a skill está acessível na sessão.
2. Rode `verify` no SQLite.
   Critério: `ok: true`.
3. Leia de volta as seções principais:
   - contas;
   - cartões;
   - empréstimos;
   - despesas recorrentes;
   - lacunas abertas.
4. Pergunte ao aluno se quer fazer um teste controlado de registro de gasto.
   Critério: não crie gasto fictício sem autorização.
5. Se houver teste autorizado, registre, verifique e leia de volta.
6. Atualize `finance_assistant_progress.json`.

## Gate de saída

Só avance para `04_crons` quando:

- runtime está instalada ou disponível;
- SQLite passa em `verify` depois da instalação;
- seções principais foram lidas;
- teste foi executado ou o aluno decidiu pular explicitamente.

## Se falhar

Não crie crons. Informe o bloqueio e a próxima ação física.
