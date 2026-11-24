# desfaz

## Turno 1 (inicial, 57 s, 15382 tokens no maior prompt)

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

## Turno 2 (alterar, 29 s, 4961 tokens no maior prompt)

**Usuário:** Mude os inativos para 21 dias.

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
    frequencia de 21 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 30 dias, 28 dias" para "Inativos: sem compra há mais de 30 dias, 21 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 21 dias`

**Notas:**
1. Premissa: Mantive `time "padrao"` e `carteira "padrao"` conforme a versão anterior, já que o usuário não respondeu à pergunta sobre a configuração de time/carteira.
2. Atualização: A frequência da regra "Inativos" foi alterada de 28 para 21 dias, conforme solicitado.
3. Nenhuma cláusula do pedido ficou de fora.

**Verificações:**
- [x] Inativos: {"dias": 21}
- [x] Ativos intacta

## Turno 3 (desfazer, 2 s, 1097 tokens no maior prompt)

**Usuário:** Não gostei, volte para a versão anterior.

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

Voltei à versão 1, com o pedido dela:
- Ativos: compra nos últimos 30 dias, 14 dias
- Inativos: sem compra há mais de 30 dias, 28 dias

**Verificações:**
- [x] arquivo do turno 1
- [x] arquivo difere do turno 2

## Turno 4 (alterar, 29 s, 5028 tokens no maior prompt)

**Usuário:** Agora mude os ativos para 10 dias.

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
    frequencia de 10 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 10 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 10 dias`

**Notas:**
1. Premissa: Mantive o time "padrao" e a carteira "padrao" conforme a versão anterior, já que o usuário não especificou alteração.
2. A frequência da regra "Ativos" foi alterada de 14 para 10 dias conforme solicitado.
3. A regra "Inativos" permaneceu inalterada (28 dias) pois o pedido anterior foi restaurado (versão 1).

**Verificações:**
- [x] Ativos: {"dias": 10}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] sem o 21
