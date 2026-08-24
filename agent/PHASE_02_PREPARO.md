# PHASE 02, Preparo

## Entrada

Use esta fase quando o Misamplace foi coletado ou as lacunas abertas estão registradas.

## Objetivo

Transformar dados coletados em um SQLite auditável e preparar o profile `assistente-financeiro` para operar sozinho.

## Arquivos do repo a ler

1. `PROCESS.yaml`
2. `CHECKPOINT_SCHEMA.json`
3. `skills/assistente-financeiro-meta/SKILL.md`
4. `skills/assistente-financeiro-meta/scripts/finance_db.py`
5. `scripts/install_skills.py`

## Procedimento

1. Instale ou copie a skill `assistente-financeiro-meta` para o profile ativo.
   Critério: diretório da skill existe no profile ou a skill está acessível na sessão.
2. Normalize os dados do Misamplace em documento JSON.
   Critério: documento contém `meta`, `pessoa`, `contas`, `cartoes`, `emprestimos`, `receitas`, `despesas_recorrentes`, `gastos`, `lacunas_abertas` e `acoes`.
3. Crie `assets/financas.db` com `finance_db.py import`.
   Critério: import retorna `snapshot_id` e `sha256`.
4. Rode `verify`.
   Critério: `ok: true`, `integrity: ok`, `hash_matches: true`.
5. Escreva `SOUL.md` e `USER.md` do profile.
   Critério: arquivos existem ou bloqueio explícito registrado.
6. Atualize `finance_assistant_progress.json`.

## Gate de saída

Só avance para `03_operacao` quando houver evidência de:

- caminho do SQLite;
- `verify ok`;
- `snapshot_id`;
- `sha256`;
- lacunas abertas preservadas;
- `SOUL.md` e `USER.md` escritos ou bloqueio explícito.

## Resposta ao aluno

Formato curto:

```text
Fase: Preparo
SQLite: <caminho>
Snapshot: <id>
Hash: <sha256>
Lacunas: <quantidade>
Próxima ação: instalar e validar skill operacional.
```

## Se falhar

Não diga que o banco está pronto. Informe o erro verificável e uma única próxima ação física.
