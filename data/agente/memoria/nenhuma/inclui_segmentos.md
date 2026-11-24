# inclui_segmentos

## Turno 1 (inicial, 23 s, 4770 tokens no maior prompt)

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

## Turno 2 (inicial, 14 s, 3955 tokens no maior prompt)

**Usuário:** Inclua os prospects, clientes com ciclo de vida prospect, a cada 7 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Prospects - 7 dias":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

**Verificações:**
- [x] Prospects: {"dias": 7}
- [ ] Ativos intacta
- [ ] Inativos intacta

## Turno 3 (inicial, 13 s, 3802 tokens no maior prompt)

**Usuário:** Agora não agende os inadimplentes.

**Agente:**

```gobr
version 1.0

time "todos vendedores":
    vendedores todos ativados

parametros "Inadimplentes":
    do time("todos vendedores")
    quando inadimplentes
    nao agendar
```

**Verificações:**
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [ ] Ativos intacta
- [ ] Inativos intacta
- [ ] Prospects intacta
