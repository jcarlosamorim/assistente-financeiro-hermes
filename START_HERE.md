# START HERE, processo do assistente financeiro Hermes

Se você é o Hermes do aluno e recebeu a mensagem "Vamos seguir este processo <URL deste repositório>", faça este fluxo.

## Objetivo

Montar um assistente financeiro pessoal em um profile Hermes chamado `assistente-financeiro`, com SQLite local, separação PF/PJ, rotina de registro de gastos, relatório semanal HTML e cobrança diária às 20h.

## Fases Masterchef IA

1. **Misamplace**, separar o necessário.
2. **Preparo**, organizar passo a passo e criar o banco.
3. **Experimentação**, testar registro, relatório e crons.

## Como proceder

### Fase 1, Misamplace

Leia `prompts/01-systemprompt-entrevista-misamplace.md` e use-o como orientação temporária da entrevista.

Conduza o aluno para preencher ou fornecer os dados de `misamplace-template/`:

- `contas.csv`
- `cartoes.csv`
- `emprestimos.csv`
- `faturas.csv`
- `despesas_recorrentes.csv`
- `receitas.csv`
- `gastos_iniciais.csv`
- PDFs, prints e comprovantes em `arquivos/`

Pergunte uma coisa por vez. Não peça senha, token, código bancário ou acesso direto ao banco.

### Fase 2, Preparo

Instale ou copie a skill `skills/assistente-financeiro-meta/` para o diretório de skills do profile `assistente-financeiro`.

Depois use essa skill para:

1. ingerir os dados do Misamplace;
2. criar `assets/financas.db`;
3. rodar `verify`;
4. escrever `SOUL.md` e `USER.md` do profile;
5. listar lacunas abertas.

Critério de passagem: SQLite com `verify` ok, snapshot e hash informados.

### Fase 3, Operação

Instale ou copie a skill `skills/assistente-financeiro-runtime/` para o profile `assistente-financeiro`.

Depois:

1. rode `verify`;
2. leia contas, cartões, faturas, empréstimos e lacunas;
3. faça um teste de registro de gasto com autorização do usuário;
4. responda com snapshot, hash e total atualizado.

### Fase 4, Crons

Leia `prompts/05-prompt-cron-html-e-cobranca.md`.

Crie dois crons:

- relatório HTML semanal aos domingos;
- cobrança diária às 20h perguntando se houve gastos no dia.

Critério de passagem: crons listados, IDs informados e SQLite íntegro.

### Fase 5, Experimentação

Execute somente três testes, nesta ordem:

1. Leia `prompts/06-experimentacao-html-situacao-atual.md` e peça um HTML da situação financeira atual.
2. Leia `prompts/07-experimentacao-registrar-comprovante.md` e registre um gasto a partir de comprovante enviado pelo aluno.
3. Leia `prompts/08-experimentacao-recomendacao-proativa.md` e responda à pergunta: "Há algo que você me indique fazer que provavelmente eu não saiba?"

Critério final: cada teste precisa informar evidência, snapshot, hash quando houver SQLite, e uma próxima ação física. Se algum teste falhar, não avance sem declarar o bloqueio.

## Regras de evidência

- Não declare pagamento, registro, importação, criação ou cron como concluído sem ferramenta e leitura de volta.
- Dados informados pelo usuário não são prova de execução.
- Toda alteração no SQLite precisa de snapshot e hash.
- Dados financeiros detalhados ficam no SQLite, não em memória persistente.
