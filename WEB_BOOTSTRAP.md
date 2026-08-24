# Bootstrap por URL, sem anexos do processo

Este arquivo existe para impedir uma ambiguidade: o aluno não precisa anexar os arquivos do processo. O Hermes do aluno deve buscar os arquivos diretamente deste repositório público.

## Mensagem única do aluno

```text
Vamos seguir este processo: https://github.com/jcarlosamorim/assistente-financeiro-hermes
```

## Regra principal para o agente

Ao receber a URL do repositório:

1. Abra a URL do GitHub.
2. Leia `WEB_BOOTSTRAP.md`.
3. Leia `PROCESS_MANIFEST.json`.
4. Leia `PROCESS.yaml`.
5. Leia `CHECKPOINT_SCHEMA.json`.
6. Leia `START_HERE.md`.
7. Crie ou atualize `finance_assistant_progress.json`.
8. Busque os arquivos necessários pelo próprio repositório, preferencialmente pelas URLs raw.
9. Não peça para o aluno anexar `START_HERE.md`, prompts, templates, skills ou scripts que já estão neste repositório.

## O que ainda pode ser pedido ao aluno

O agente só deve pedir dados pessoais do aluno, por exemplo:

- saldo de contas;
- cartões usados;
- datas de fechamento e vencimento;
- empréstimos;
- faturas reais;
- comprovantes reais;
- prints ou PDFs financeiros do próprio aluno.

Esses dados não estão no repositório e não devem estar em repositório público.

## Se o agente não conseguir baixar arquivos

Use esta ordem de fallback:

1. `web_extract` ou web fetch comum na página do GitHub.
2. URLs raw de `raw.githubusercontent.com` listadas no `PROCESS_MANIFEST.json`.
3. Browser ou Oxylabs se GitHub bloquear, truncar ou exigir renderização.
4. Só então pedir ao aluno para copiar e colar o conteúdo do arquivo específico que falhou.

Nunca peça para o aluno anexar todos os arquivos do processo se a falha foi em apenas um arquivo.

## Critério de sucesso do bootstrap

Antes de começar a entrevista, o agente deve conseguir responder internamente:

- Qual é a fase atual?
- Qual arquivo `agent/PHASE_*.md` governa essa fase?
- Qual é o próximo gate?
- Onde está `finance_assistant_progress.json`?
- Quais arquivos do processo já foram lidos do repositório?
- Quais dados pessoais ainda dependem do aluno?
