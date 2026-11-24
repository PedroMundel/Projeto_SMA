# inclui_segmentos

## Turno 1 (inicial, 22 s, 4770 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 28 s, 4403 tokens no maior prompt)

**Usuário:** Inclua os prospects, clientes com ciclo de vida prospect, a cada 7 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

Mudança no pedido:
- incluído: "Prospects: clientes com ciclo de vida prospect, 7 dias"

O que mudou no arquivo:
- "Prospects" (parametros): incluída

**Verificações:**
- [x] Prospects: {"dias": 7}
- [x] Ativos intacta
- [x] Inativos intacta

## Turno 3 (alterar, 32 s, 4123 tokens no maior prompt)

**Usuário:** Agora não agende os inadimplentes.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

Mudança no pedido:
- incluído: "Inadimplentes: sem agendamento"

O que mudou no arquivo:
- "Inadimplentes" (parametros): incluída

**Verificações:**
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [x] Ativos intacta
- [x] Inativos intacta
- [x] Prospects intacta
- [x] Inadimplentes bloqueia antes
