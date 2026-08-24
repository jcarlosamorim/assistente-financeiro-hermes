# PHASE 01, Misamplace

## Entrada

Use esta fase quando o aluno começou o processo pelo link do repositório e ainda não existe SQLite financeiro confiável.

## Regra de condução

Faça uma pergunta por vez. Não peça anexos do processo. Busque prompts, templates e instruções no repositório. Peça ao aluno somente dados pessoais financeiros que não podem existir no GitHub público.

## Arquivos do repo a ler

1. `WEB_BOOTSTRAP.md`
2. `PROCESS_MANIFEST.json`
3. `PROCESS.yaml`
4. `CHECKPOINT_SCHEMA.json`
5. `prompts/01-systemprompt-entrevista-misamplace.md`
6. Templates em `misamplace-template/`

## Checklist de coleta

Coletar ou registrar lacuna para:

- nome e forma de tratamento;
- separação PF e PJ;
- saldos atuais em bancos PF;
- saldos atuais em bancos PJ;
- cartões PF;
- cartões PJ;
- dia de fechamento e vencimento de cada cartão;
- empréstimos pendentes;
- receitas;
- despesas recorrentes;
- faturas atuais;
- gastos recentes ainda não postados.

## Perguntas recomendadas

Use perguntas modulares, com exemplos. Evite perguntas abertas como “quais contas bancárias você usa?”. Primeiro descubra a estrutura, depois colete cada módulo.

### Módulo 1, separação PF/PJ

Comece com:

```text
Vamos montar seu Misamplace financeiro por partes.

Primeiro: você tem contas separadas para PF e PJ?

Pode responder em um destes formatos:
1. Tenho PF e PJ.
2. Tenho só PF.
3. Tenho só PJ.
4. Ainda misturo tudo na mesma conta.
```

Depois, se houver PF:

```text
Agora me mande as contas PF, uma por linha, neste formato:
Banco | tipo de conta | saldo aproximado | data do saldo

Exemplo:
Nubank | conta corrente PF | R$ 1.250,00 | hoje
Itaú | poupança PF | R$ 3.000,00 | 23/08
```

Se houver PJ:

```text
Agora me mande as contas PJ, uma por linha, neste formato:
Banco | tipo de conta | saldo aproximado | data do saldo

Exemplo:
Nubank PJ | conta PJ | R$ 4.800,00 | hoje
Inter PJ | conta PJ | R$ 900,00 | 23/08
```

### Módulo 2, cartões e faturas

Não pergunte “qual é o valor atual em aberto da fatura de cada cartão?” como pergunta solta. Peça a fatura, porque um único arquivo alimenta vários campos.

Pergunte:

```text
Agora vamos mapear cartões.

Para cada cartão que você usa, me envie a fatura atual em PDF, print ou CSV, e junto escreva:
- nome do cartão ou banco;
- se é PF ou PJ;
- dia que a fatura fecha;
- dia de vencimento.

Exemplo:
Bradesco Visa | PF | fecha dia 28 | vence dia 10 | fatura anexada
Nubank PJ | PJ | fecha dia 04 | vence dia 11 | fatura anexada
```

Ao receber a fatura, o agente deve extrair:

- valor atual da fatura;
- compras lançadas;
- parcelamentos em andamento;
- juros, IOF e encargos;
- vencimento, se constar no arquivo;
- fechamento, se constar no arquivo;
- lacunas entre o informado e o arquivo.

### Módulo 3, empréstimos

Pergunte com exemplo:

```text
Você tem empréstimos, financiamentos ou parcelamentos bancários em aberto?

Responda assim:
Banco | PF/PJ | saldo devedor aproximado | parcela | parcelas restantes | vencimento

Exemplo:
Itaú | PF | R$ 8.000,00 | R$ 620,00 | 14 | dia 15
```

### Módulo 4, recorrências

Pergunte com exemplo:

```text
Agora me mande contas fixas e assinaturas recorrentes.

Formato:
Descrição | PF/PJ | valor | frequência | conta ou cartão | vencimento

Exemplo:
Internet | PF | R$ 120,00 | mensal | Nubank PF | dia 10
Google Workspace | PJ | R$ 75,00 | mensal | Nubank PJ | dia 5
```

Depois siga uma pergunta por vez, priorizando o gate pendente. Cada pergunta deve ter um exemplo de resposta.

## Atualização do checkpoint

Depois de cada resposta útil, atualize `finance_assistant_progress.json`:

- `current_state`: `01_misamplace`
- `pending_gates`: gate ainda faltante;
- `open_gaps`: lacunas explícitas;
- `last_user_message_summary`;
- `last_assistant_action_summary`.

## Gate de saída

Só avance para `02_preparo` quando:

- PF/PJ foram identificados ou lacuna registrada;
- pelo menos uma conta ou cartão foi registrado, ou ausência de ambos foi registrada como lacuna;
- datas de fechamento e vencimento foram pedidas para cada cartão conhecido;
- lacunas abertas foram listadas;
- o aluno confirmou que pode seguir para criar o banco inicial.

## Se falhar

Não avance. Faça uma única pergunta concreta ou peça um único documento pessoal específico.
