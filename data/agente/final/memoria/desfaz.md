# desfaz

## Turno 1 (inicial, 23 s, 4750 tokens no maior prompt)

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

## Turno 2 (alterar, 26 s, 4714 tokens no maior prompt)

**Usuário:** Mude os inativos para 21 dias.

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
    frequencia de 21 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 30 dias, 28 dias" para "Inativos: sem compra há mais de 30 dias, 21 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 21 dias`

**Verificações:**
- [x] Inativos: {"dias": 21}
- [x] Ativos intacta

## Turno 3 (desfazer, 2 s, 1056 tokens no maior prompt)

**Usuário:** Não gostei, volte para a versão anterior.

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

Voltei à versão 1, com o pedido dela:
- Ativos: compra nos últimos 30 dias, 14 dias
- Inativos: sem compra há mais de 30 dias, 28 dias

**Verificações:**
- [x] arquivo do turno 1
- [x] arquivo difere do turno 2

## Turno 4 (alterar, 26 s, 4781 tokens no maior prompt)

**Usuário:** Agora mude os ativos para 10 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 10 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 10 dias`

**Verificações:**
- [x] Ativos: {"dias": 10}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] sem o 21
