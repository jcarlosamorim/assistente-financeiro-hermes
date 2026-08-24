# Experimentação 02, registrar gasto por comprovante

## Prompt para o aluno

Envie ao Hermes do profile `assistente-financeiro`:

```text
Vou mandar um comprovante. Registre esse gasto no lugar correto.
```

Depois anexe o comprovante, cupom, print ou PDF.

## O que o assistente deve fazer

1. Carregar a skill `assistente-financeiro-runtime`.
2. Rodar `verify` no SQLite antes de alterar qualquer dado.
3. Ler o comprovante com ferramenta adequada.
4. Extrair, quando disponível:
   - data;
   - valor;
   - estabelecimento ou fornecedor;
   - forma de pagamento;
   - cartão ou conta;
   - categoria provável;
   - evidência usada.
5. Se faltar cartão, conta ou escopo PF/PJ, perguntar apenas o dado faltante.
6. Registrar o gasto no local correto do SQLite.
7. Recalcular total da fatura ou saldo teórico afetado.
8. Rodar `verify` novamente.
9. Ler de volta o campo alterado.
10. Responder com snapshot, hash, local do registro e total atualizado.

## Critério de sucesso

A etapa só passa se:

- o gasto estiver no SQLite;
- o campo alterado foi lido de volta;
- a soma foi calculada por ferramenta;
- `verify` retornou ok depois da escrita;
- a resposta traz snapshot e hash.

## Se falhar

Não diga que registrou. Explique o bloqueio e peça uma única próxima ação física.
