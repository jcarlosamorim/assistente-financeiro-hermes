# Etapa 05, criar crons do assistente financeiro

## Prompt para o aluno

Anexe este arquivo quando o SQLite já estiver criado, verificado e a skill operacional já estiver instalada. Depois escreva apenas:

```text
siga
```

## O que o assistente deve fazer

Ao receber `siga`, leia este arquivo inteiro e crie as rotinas de relatório HTML semanal e cobrança diária às 20h. Depois liste os crons, rode testes manuais e informe IDs e evidências.

---

# Prompt para criação dos crons do assistente financeiro

Use este prompt depois que o Misamplace foi ingerido, o SQLite foi verificado e a skill operacional está instalada.

## Objetivo

Criar duas rotinas autônomas no profile `assistente-financeiro`:

1. **Relatório HTML semanal**, todo domingo, com posição financeira, faturas, gastos por categoria, lacunas e próximos vencimentos.
2. **Cobrança diária às 20h**, perguntando se houve gastos no dia e registrando somente quando o usuário responder.

## Cron 1: relatório semanal HTML

Schedule sugerido:

```text
0 9 * * 0
```

Prompt do cron:

```text
Use a skill assistente-financeiro-runtime. Verifique o SQLite com `verify`. Gere um HTML semanal a partir do estado atual, sem expor dados sensíveis além do necessário. O relatório deve conter: resumo PF/PJ, saldo líquido, faturas abertas, gastos da semana, recorrências próximas, lacunas abertas e ações recomendadas. Salve o HTML em `~/relatorios-financeiros/relatorio-financeiro-AAAA-MM-DD.html`. Entregue a mensagem com caminho do arquivo, snapshot, hash e três próximas ações físicas. Se a verificação falhar, não gere relatório e informe o erro.
```

## Cron 2: cobrança diária de gastos

Schedule sugerido:

```text
0 20 * * *
```

Prompt do cron:

```text
Use a skill assistente-financeiro-runtime. Envie uma pergunta curta: "Teve gasto hoje? Se sim, me mande valor, cartão/conta e descrição." Não invente gastos. Se o usuário responder com gasto, registrar no SQLite, verificar, e responder com snapshot, hash, conta/cartão e total atualizado. Se não houver resposta ou se o usuário disser que não teve gasto, não registrar nada.
```

## Verificação após criar os crons

Depois da criação:

1. Liste os crons.
2. Rode manualmente o relatório semanal uma vez.
3. Confira se o HTML foi gerado.
4. Rode manualmente a cobrança diária uma vez.
5. Confirme que ela não registra gasto sem resposta do usuário.

## Critério de conclusão

A rotina só está pronta quando houver prova de:

- cron semanal criado com ID;
- cron diário criado com ID;
- execução de teste do HTML com caminho do arquivo;
- execução de teste da cobrança sem registro indevido;
- SQLite íntegro após os testes.

