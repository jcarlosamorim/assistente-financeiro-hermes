# Assistente financeiro pessoal com Hermes Agent

Material público da aula para montar um assistente financeiro pessoal com Hermes Agent.

## Para o aluno

No seu Hermes, envie:

```text
Vamos seguir este processo: https://github.com/jcarlosamorim/assistente-financeiro-hermes
```

O repositório substitui os anexos do processo. O Hermes deve ler `WEB_BOOTSTRAP.md`, `PROCESS_MANIFEST.json` e `START_HERE.md` diretamente do GitHub. Você só precisa enviar seus dados pessoais financeiros quando ele pedir, como saldos, faturas reais, comprovantes e prints.

Depois responda às perguntas do assistente.

## Para quem publica o repositório

Troque `SEU_USUARIO` pelo usuário ou organização real do GitHub depois de publicar.

## Estrutura

```text
START_HERE.md
WEB_BOOTSTRAP.md
PROCESS_MANIFEST.json
prompts/
  01-systemprompt-entrevista-misamplace.md
  05-prompt-cron-html-e-cobranca.md
  06-experimentacao-html-situacao-atual.md
  07-experimentacao-registrar-comprovante.md
  08-experimentacao-recomendacao-proativa.md
misamplace-template/
  contas.csv
  cartoes.csv
  emprestimos.csv
  faturas.csv
  despesas_recorrentes.csv
  receitas.csv
  gastos_iniciais.csv
skills/
  assistente-financeiro-meta/
  assistente-financeiro-runtime/
```

## Fluxo

1. Criar profile `assistente-financeiro`.
2. Conectar novo bot do Telegram, se desejado.
3. Mandar o link deste repositório para o Hermes do aluno.
4. O Hermes lê `START_HERE.md` e conduz o processo.
5. O aluno fornece dados do Misamplace.
6. O Hermes instala as skills, cria o SQLite e agenda os crons.
7. O aluno executa os três prompts de experimentação: HTML atual, registro por comprovante e recomendação proativa.

## Segurança

Este repositório não contém dados financeiros reais nem credenciais. Os dados do aluno devem ser coletados no ambiente local dele e gravados no SQLite do profile dele.
