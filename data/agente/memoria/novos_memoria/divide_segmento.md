# divide_segmento

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

## Turno 2 (alterar, 66 s, 6171 tokens no maior prompt)

**Usuário:** Separe os inativos em dois: sem compra entre 60 e 120 dias, a cada 21 dias, e sem compra há mais de 120 dias, a cada 45 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos (60-120 dias)":
    do time("televendas")
    quando recencia de positivacao entre 61 dias e 120 dias
    frequencia de 21 dias

parametros "Inativos (>120 dias)":
    do time("televendas")
    frequencia de 45 dias
```

Mudança no pedido:
- removido: "Inativos: sem compra há mais de 60 dias, 28 dias"
- incluído: "Inativos (60-120 dias): sem compra entre 60 e 120 dias, 21 dias"
- incluído: "Inativos (>120 dias): sem compra há mais de 120 dias, 45 dias"

O que mudou no arquivo:
- "Inativos (60-120 dias)" (parametros): incluída
- "Inativos (>120 dias)" (parametros): incluída
- "Inativos" (parametros): removida

**Verificações:**
- [x] Ativos intacta
- [x] sem o 28
- [x] com o 120
- [x] com o 21
- [x] com o 45
