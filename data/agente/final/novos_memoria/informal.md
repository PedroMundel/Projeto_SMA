# informal

## Turno 1 (inicial, 26 s, 4750 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 26 s, 4677 tokens no maior prompt)

**Usuário:** muda os ativo p 20 dias blz

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 20 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 20 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 20 dias`

**Verificações:**
- [x] Ativos: {"dias": 20}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] sem o 14

## Turno 3 (alterar, 45 s, 9473 tokens no maior prompt)

**Usuário:** bloqueia quem ta baixado na receita

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Não agendar Filiais":
    do time("televendas")
    quando e o cliente filial
    nao agendar

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 20 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- incluído: "Filiais: não agendar"

O que mudou no arquivo:
- "Não agendar Filiais" (parametros): incluída

- "Filiais: não agendar": o GoBR não tem cláusula para identificar "filial" genericamente; usei `quando e o cliente filial` baseado no exemplo regra_180, que é o filtro padrão para isso.
- A ordem das regras foi ajustada: o bloqueio de filiais vem primeiro para garantir que filiais não sejam agendadas mesmo que se enquadrem nos critérios de Ativos ou Inativos.
- As regras de Ativos e Inativos mantiveram os critérios e frequências do pedido (30 dias/20 dias e 30 dias/28 dias).

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Filiais": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Filiais": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 20}
- [x] Inativos: {"dias": 28}
- [x] Ativos intacta
- [x] Inativos intacta
