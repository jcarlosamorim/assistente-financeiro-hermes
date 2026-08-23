---
name: assistente-financeiro-meta
description: Ingira Misamplace financeiro em SQLite auditável.
version: 0.1.0
author: José Carlos Amorim, Hermes Agent
license: Proprietary
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [financas, misamplace, sqlite, onboarding]
    related_skills: []
---

# Assistente Financeiro Meta

Esta skill é usada somente na fase de Misamplace. Ela entrevista, valida e cria o primeiro snapshot financeiro do usuário em SQLite. Não é a skill operacional diária.

## Quando usar

- Profile `assistente-financeiro` ainda está zerado.
- Usuário subiu CSVs, PDFs, prints ou um zip de Misamplace.
- É preciso criar `assets/financas.db` pela primeira vez.
- Não use para: registrar gastos diários depois que a skill runtime já estiver instalada.

## Banco canônico

```text
assets/financas.db
scripts/finance_db.py
```

## Procedimento

1. Verifique se existe `assets/financas.db`.
   Critério: se não existir, prepare `dados_iniciais.json` para importação.
2. Leia os arquivos do Misamplace.
   Critério: saldos, cartões, faturas, empréstimos e recorrências foram separados em PF/PJ.
3. Normalize o documento financeiro.
   Critério: o JSON contém `meta`, `contas`, `cartoes`, `emprestimos`, `receitas`, `despesas_recorrentes`, `gastos`, `lacunas_abertas` e `acoes`.
4. Importe no SQLite.
   Critério: `python scripts/finance_db.py import ...` retorna snapshot e hash.
5. Rode `verify`.
   Critério: integridade ok, `hash_matches: true`, um único snapshot atual.
6. Escreva `SOUL.md` e `USER.md` do profile.
   Critério: ambos refletem separação PF/PJ, evidência, preferências e lacunas.

## Comandos

```bash
python scripts/finance_db.py --db assets/financas.db verify
python scripts/finance_db.py --db assets/financas.db summary
python scripts/finance_db.py --db assets/financas.db import /caminho/dados_iniciais.json --source "Misamplace inicial" --effective-date AAAA-MM-DD --note "snapshot inicial"
```

## Regras

- Nunca pedir senha, token ou código bancário.
- Nunca dizer que pagamento foi executado sem comprovante.
- Registrar fatos como `informado pelo usuário`, `comprovado por arquivo` ou `reconciliado por extrato`.
- Lacunas não bloqueiam o banco: registre-as em `lacunas_abertas`.
- Dados financeiros detalhados ficam no SQLite, não em memória persistente.

## Verificação

- [ ] `verify` ok
- [ ] snapshot inicial existe
- [ ] SOUL.md criado
- [ ] USER.md criado
- [ ] lacunas listadas
- [ ] usuário recebeu resumo do Misamplace
