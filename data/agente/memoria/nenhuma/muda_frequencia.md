# muda_frequencia

## Turno 1 (inicial, 58 s, 15382 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

carteira "padrao":
    clientes carteirafixa("padrao")

parametros "Ativos":
    da carteira("padrao")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

**Premissas:**
1. Como o usuário não especificou o time ou a carteira, assumi a criação de um time "padrao" com todos os vendedores e uma carteira "padrao" vinculada a esse time, que é uma estrutura comum em regras GoBR quando não há especificação.
2. As cláusulas de frequência e critérios de atividade/inatividade foram mantidas conforme o pedido e validadas pelos exemplos.

Perguntas feitas:
- Qual é o nome da carteira e do time que devem ser usados nas regras? (Ex: time "televendas", carteira "televendas") -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Como devo definir o time e a carteira para as regras de Ativos e Inativos? Posso usar `time "padrao": vendedores todos` e `carteira "padrao": clientes carteirafixa("padrao")`? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 22 s, 3441 tokens no maior prompt)

**Usuário:** Troque os ativos para 15 dias.

**Agente:**

```gobr
version 1.0

time "empresa toda":
    vendedores todos

parametros "Ativos: 15 dias":
    da carteira("empresa toda")
    quando ativos para o vendedor
    frequencia de 15 dias
```

**Notas:**
1. **Premissa assumida:** Como o pedido não especificou um time ou carteira, assumi `vendedores todos` e uma carteira genérica ("empresa toda") para abranger todos os clientes ativos.
2. **Critério de Atividade:** O pedido apenas dizia "ativos". Utilizei a cláusula `ativos para o vendedor` (padrão do manual 6.1), pois é a mais comum para regras de frequência individual. Se a regra for para a empresa toda, poderia ser `ativos para a empresa`.
3. **Frequência:** O pedido pediu "15 dias". A cláusula `frequencia de 15 dias` foi utilizada conforme os exemplos (ex: regra_134).
4. **Segmentos faltantes:** O pedido original parecia ser um fragmento ("Troque os ativos para 15 dias"). Regras para "Inativos" ou "Sem Vendas" não foram incluídas pois não foram solicitadas explicitamente neste trecho, apenas a modificação para ativos. Se houver outras faixas, elas devem ser adicionadas como novas regras `parametros`.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Ativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 15}
- [ ] Inativos: {"dias": 28}
- [ ] Inativos intacta
- [x] sem o 14

## Turno 3 (inicial, 25 s, 4087 tokens no maior prompt)

**Usuário:** E os inativos, ficaram a cada quantos dias?

**Agente:**

```gobr
Version 1.0

time "empresa toda":
    vendedores todos

carteira "empresa toda":
    clientes carteirafixa("empresa toda")

parametros "Regra para inativos":
    da carteira("empresa toda")
    quando inativos para o vendedor
    frequencia de 45 dias
    preferencia do vendedor
```

Premissa assumida: Como o usuário não respondeu e o GoBR não tem um valor padrão para inatividade, assumi a frequência de 45 dias, que é um valor comum em regras de inativos vistas nos exemplos (ex: regra_074).

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.

Perguntas feitas:
- Qual a frequência de agendamento (em dias) desejada para clientes inativos? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] arquivo do turno 2
- [ ] resposta tem 28
