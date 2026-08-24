# Experimentação 03, recomendação proativa

## Prompt para o aluno

Envie ao Hermes do profile `assistente-financeiro`:

```text
Há algo que você me indique fazer que provavelmente eu não saiba?
```

## O que o assistente deve fazer

1. Carregar a skill `assistente-financeiro-runtime`.
2. Rodar `verify` no SQLite.
3. Ler somente os campos necessários para análise:
   - lacunas abertas;
   - faturas próximas;
   - empréstimos;
   - recorrências;
   - saldos;
   - ações pendentes.
4. Procurar um ponto cego financeiro provável.
5. Responder com exatamente uma recomendação principal.
6. A recomendação precisa passar por três portões:
   - soberania, deixa o usuário mais independente ou mais dependente?
   - riqueza versus status, cria ativo ou só aplauso?
   - entusiasmo binário, é um sim claro ou não?
7. Encerrar com uma única próxima ação física.

## Critério de sucesso

A etapa só passa se:

- a recomendação usa dados do SQLite;
- o assistente não despeja uma lista genérica;
- há uma única ação física no final;
- a resposta deixa claro qual dado sustentou a recomendação.

## Se falhar

Se os dados forem insuficientes, diga qual lacuna impede recomendação confiável e peça uma única informação.
