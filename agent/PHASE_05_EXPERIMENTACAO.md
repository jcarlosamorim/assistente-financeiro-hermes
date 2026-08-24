# PHASE 05, Experimentação

## Entrada

Use esta fase quando o runtime funciona e os crons foram criados ou o bloqueio do scheduler foi registrado.

## Objetivo

Executar somente três testes, em ordem, para provar que o assistente financeiro está útil no mundo real.

## Arquivos do repo a ler

1. `PROCESS.yaml`
2. `prompts/06-experimentacao-html-situacao-atual.md`
3. `prompts/07-experimentacao-registrar-comprovante.md`
4. `prompts/08-experimentacao-recomendacao-proativa.md`

## Teste 1, HTML da situação financeira atual

Siga `prompts/06-experimentacao-html-situacao-atual.md`.

Gate:

- HTML existe;
- caminho do arquivo informado;
- SQLite `verify ok`;
- snapshot e hash informados.

## Teste 2, comprovante para registrar gasto

Siga `prompts/07-experimentacao-registrar-comprovante.md`.

Gate:

- comprovante lido;
- gasto registrado no lugar correto;
- campo alterado lido de volta;
- total recalculado;
- snapshot e hash informados.

Se o aluno ainda não tem comprovante, pare aqui e peça um único comprovante real.

## Teste 3, recomendação proativa

Siga `prompts/08-experimentacao-recomendacao-proativa.md`.

Gate:

- recomendação baseada em dados do SQLite;
- exatamente uma recomendação principal;
- exatamente uma próxima ação física;
- lacuna declarada se dados forem insuficientes.

## Atualização do checkpoint

Registre resultado de cada teste em `experiment_tests`:

- `status`: `passed`, `failed` ou `blocked`;
- evidência;
- snapshot e hash quando houver;
- próxima ação.

## Critério final

A aula termina quando os três testes passam ou quando o bloqueio restante é claro e acionável.
