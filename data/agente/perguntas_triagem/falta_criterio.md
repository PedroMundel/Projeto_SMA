```gobr
version 1.0

time "padrao":
    vendedores todos

carteira "carteira padrao":
    clientes portfolio("padrao")

parametros "Ativos":
    da carteira("carteira padrao")
    quando atividade do vendedor de 60 dias
    frequencia de 14 dias

parametros "Inativos":
    da carteira("carteira padrao")
    frequencia de 28 dias
```

O manual confirma a existência da cláusula `atividade do vendedor de 60 dias`, que corresponde exatamente à definição de "quem comprou do vendedor no período especificado" (últimos 60 dias). Isso resolve a divergência apontada pelo conferente.

A regra "Ativos" deve usar `quando atividade do vendedor de 60 dias`.
A regra "Inativos" deve pegar os clientes que sobrarem (não se enquadram em "Ativos"). Como o pedido define "Inativos" como "quem não comprou nesse período" (ou seja, não comprou nos últimos 60 dias), e as regras rodam em ordem, a regra de "Inativos" pode ser uma regra final sem `quando` (ou com `quando` genérico, mas a prática nos exemplos é deixar a última regra sem `quando` para pegar os demais). No entanto, para ser explícito e seguir a estrutura de segmentação, podemos usar `quando inativos para o vendedor` se quiséssemos o critério padrão, mas o pedido define inativo como *não comprou nos últimos 60 dias*. A cláusula `atividade do vendedor de 60 dias` captura quem *teve* compra. Quem não tem essa compra é o "inativo" para este critério específico. Nos exemplos, a regra final muitas vezes não tem `quando`. Vou usar a regra final sem `quando` para "Inativos" para garantir que pegue todos que não foram ativos (não compraram nos últimos 60 dias).

Correção:
1. Regra "Ativos": `quando atividade do vendedor de 60 dias`
2. Regra "Inativos": Sem `quando` (regra final) ou `quando inativos para o vendedor`? O pedido diz "Inativos: 28 dias" e define inativo como "não comprou nesse período". Se eu usar `atividade do vendedor de 60 dias` para ativos, os demais são inativos. A regra final sem `quando` é a forma correta de pegar os demais.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
- "Inativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Ativo é quem comprou nos últimos 60 dias; inativo é quem não comprou nesse período.