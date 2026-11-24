# pedido_novo

## Turno 1 (inicial, 52 s, 15382 tokens no maior prompt)

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

## Turno 2 (novo, 25 s, 3977 tokens no maior prompt)

**Usuário:** Esqueça esse pedido, é outro cliente. Novo pedido:
Prospects: clientes com ciclo de vida prospect, 7 dias
Não agendar inadimplentes

**Agente:**

```gobr
version 1.0

time "todos vendedores":
    vendedores todos ativados

parametros "Não agendar inadimplentes":
    do time("todos vendedores")
    quando inadimplentes
    nao agendar

parametros "Prospects":
    do time("todos vendedores")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

Inadimplentes: o pedido não especifica o time para a regra de bloqueio; assumi "todos vendedores" por padrão.

**Verificações:**
- [x] Prospects: {"dias": 7}
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [x] sem regra Ativos
- [x] sem regra Inativos
- [x] sem o 14
- [x] sem o 28
