# informal

## Turno 1 (inicial, 55 s, 15382 tokens no maior prompt)

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

## Turno 2 (inicial, 24 s, 4984 tokens no maior prompt)

**Usuário:** muda os ativo p 20 dias blz

**Agente:**

```gobr
version 1.0


time "padrao":
    vendedores todos


parametros "Ativos":
    do time("padrao")
    quando ativos para o vendedor
    frequencia de 20 dias
```

**Notas:**
1. **Time:** Como o pedido não especificou um time (ex: "televendas", "campo"), assumi um time genérico "padrao" com todos os vendedores. Ajuste se necessário.
2. **Segmento:** O pedido pediu para mudar "ativos" para 20 dias. Criei a regra `parametros "Ativos"` usando a cláusula `ativos para o vendedor` (presente nos exemplos) e `frequencia de 20 dias`.
3. **Ordem:** Esta regra deve vir após quaisquer regras de bloqueio (inadimplentes, filiais, etc.) se existirem no contexto completo, pois "ativos" é uma condição de estado positivo. Se houver outras regras para "ativos" com frequências diferentes baseadas em outros critérios (ex: valor de compra), elas devem vir antes desta regra genérica.
4. **Ausência de outros critérios:** O pedido foi breve ("muda os ativo p 20 dias"). Não foram incluídos filtros adicionais (como tipo de pessoa, carteira, etc.) pois não foram solicitados. Se houver necessidade de segmentação fina, por favor, especifique.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Ativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 20}
- [ ] Inativos: {"dias": 28}
- [ ] Inativos intacta
- [x] sem o 14

## Turno 3 (inicial, 23 s, 7672 tokens no maior prompt)

**Usuário:** bloqueia quem ta baixado na receita

**Agente:**

```gobr
Version 1.0

time "padrao":
    vendedores todostelevendas ativados

parametros "bloqueia quem ta baixado na receita":
    do time("padrao")
    quando status na receita federal definido como baixada
    nao agendar
```

**Verificações:**
- [ ] Ativos: {"dias": 20}
- [ ] Inativos: {"dias": 28}
- [ ] Ativos intacta
- [ ] Inativos intacta
