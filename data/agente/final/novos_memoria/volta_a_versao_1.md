# volta_a_versao_1

## Turno 1 (inicial, 27 s, 4750 tokens no maior prompt)

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

## Turno 2 (alterar, 26 s, 4758 tokens no maior prompt)

**Usuário:** Ativos a cada 9 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 9 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 9 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 9 dias`

**Verificações:**
- [x] Ativos: {"dias": 9}
- [x] Inativos intacta

## Turno 3 (alterar, 27 s, 4962 tokens no maior prompt)

**Usuário:** E inativos a cada 40.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 9 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 40 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 30 dias, 28 dias" para "Inativos: sem compra há mais de 30 dias, 40 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 40 dias`

**Verificações:**
- [x] Inativos: {"dias": 40}
- [x] Ativos intacta

## Turno 4 (desfazer, 2 s, 1115 tokens no maior prompt)

**Usuário:** Volta tudo para a versão 1.

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
- [x] arquivo difere do turno 3
