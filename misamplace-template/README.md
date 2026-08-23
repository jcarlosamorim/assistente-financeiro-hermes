# Misamplace financeiro

Preencha estes arquivos antes da entrevista com o assistente.

## O que separar

1. Saldos atuais de todos os bancos, PF e PJ.
2. Empréstimos pendentes em todos os bancos.
3. Faturas de todos os cartões.
4. Data que fecha a fatura e vencimento de cada cartão.
5. Receitas, contas fixas e assinaturas.
6. Gastos recentes que ainda não aparecem em fatura ou extrato.

## Nomes de arquivos

Use este padrão:

```text
fatura_cartao_<nomebanco>.pdf
extrato_conta_<nomebanco>.pdf
comprovante_<descricao_curta>.pdf
```

Exemplos:

```text
fatura_cartao_nubank_pj.pdf
fatura_cartao_bradesco_pf.pdf
extrato_conta_itau_pf.pdf
```

## Como usar

1. Preencha os CSVs.
2. Coloque PDFs e imagens dentro de `arquivos/`.
3. Compacte a pasta `misamplace/`.
4. Envie para o profile `assistente-financeiro` com o system prompt de entrevista.
