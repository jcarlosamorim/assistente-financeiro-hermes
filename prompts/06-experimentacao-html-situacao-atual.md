# Experimentação 01, HTML da situação financeira atual

## Prompt para o aluno

Envie ao Hermes do profile `assistente-financeiro`:

```text
Gere um HTML da minha situação financeira atual.
```

## O que o assistente deve fazer

1. Carregar a skill `assistente-financeiro-runtime`.
2. Rodar `verify` no SQLite antes de qualquer leitura.
3. Gerar um HTML com a posição financeira atual.
4. Incluir, no mínimo:
   - resumo PF e PJ;
   - saldos por conta;
   - faturas abertas por cartão;
   - empréstimos pendentes;
   - despesas recorrentes;
   - lacunas abertas;
   - três próximas ações físicas.
5. Salvar o HTML em `~/relatorios-financeiros/`.
6. Responder com caminho do arquivo, snapshot, hash e status da verificação.

## Critério de sucesso

A etapa só passa se:

- o arquivo HTML existir;
- o SQLite tiver `verify` ok;
- a resposta trouxer snapshot e hash;
- o relatório não expuser senha, token, chave, documento fiscal ou credencial bancária.

## Se falhar

Não invente relatório. Diga qual verificação falhou e qual é a próxima ação física do aluno.
