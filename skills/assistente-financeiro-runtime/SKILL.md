---
name: assistente-financeiro-runtime
description: Registre gastos e reconcilie finanças pessoais.
version: 0.1.0
author: José Carlos Amorim, Hermes Agent
license: Proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [financas, gastos, cartoes, relatorios]
    related_skills: []
---

# Assistente Financeiro Runtime

Skill operacional para registrar gastos, consultar faturas, reconciliar extratos e gerar relatório HTML semanal. Use somente depois que o Misamplace inicial foi ingerido.

## Quando usar

- Usuário informa gasto novo.
- Usuário envia cupom, fatura, extrato ou comprovante.
- Usuário pede posição financeira, fatura, saldo ou relatório.
- Cron semanal precisa gerar HTML.
- Cron diário das 20h precisa cobrar gastos do dia.

## Banco canônico

```text
assets/financas.db
scripts/finance_db.py
```

## Fluxo obrigatório

```text
pedido financeiro
  -> rodar verify
  -> ler só o campo necessário
  -> classificar PF/PJ, conta/cartão, categoria e competência
  -> registrar via set/import criando snapshot
  -> rodar verify novamente
  -> ler de volta o campo alterado
  -> responder com snapshot, hash, total alterado e lacunas
```

## Registro de gasto

1. Identifique data, valor, descrição, escopo PF/PJ e forma de pagamento.
   Critério: sem esses campos, registre lacuna ou pergunte uma coisa só.
2. Classifique no lugar correto.
   Critério: cartão vira fatura do cartão; débito vira conta; recorrente atualiza recorrências.
3. Preserve evidência.
   Critério: `evidencia` diz se foi informado, cupom, PDF, print ou extrato.
4. Atualize total da fatura ou saldo teórico.
   Critério: soma bate com os lançamentos.
5. Verifique e leia de volta.
   Critério: `verify` ok e campo alterado contém o gasto.

## Relatório HTML

Use:

```bash
python scripts/generate_weekly_html.py
```

O gerador deve produzir um painel visual em dark mode no padrão do painel financeiro original: cards de faturas no topo, tabelas detalhadas por cartão, seção de contas, gastos fixos mensais, lacunas abertas, próximas ações físicas e rodapé com snapshot, hash, competência e data de atualização.

O gerador deve aceitar o campo canônico `fatura_atual` em cada cartão. Para compatibilidade com instalações antigas, ele também tolera chaves legadas como `fatura_setembro`, `fatura_agosto` e `faturas_detalhadas`. Quando a fatura não tiver total explícito, o script calcula o total a partir de `lancamentos`, `itens`, `compras`, `despesas`, `parcelamentos` e `creditos`.

Critério: o script retorna JSON com `ok`, `output`, `snapshot_id` e `sha256`, e o HTML usa somente os dados do SQLite do aluno instalado.

## Cobrança diária

Às 20h, pergunte apenas:

```text
Teve gasto hoje? Se sim, me mande valor, cartão/conta e descrição.
```

Não registre nada sem resposta do usuário.

## Regras

- Não pedir senha, token ou código bancário.
- Não registrar pagamento como executado sem comprovante.
- Separar PF e PJ sempre.
- Dados financeiros detalhados ficam no SQLite, não em memória persistente.
- Toda conclusão operacional precisa de snapshot e hash.

## Verificação

- [ ] `verify` ok antes e depois
- [ ] snapshot novo criado quando houve alteração
- [ ] campo alterado lido de volta
- [ ] totais recalculados por ferramenta
- [ ] resposta cita snapshot e hash
