# duvida_de_cascata

## Turno 1 (inicial, 30 s, 4736 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Risco: última compra entre 30 e 60 dias, 7 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Risco: {"dias": 7}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 29 s, 4717 tokens no maior prompt)

**Usuário:** Um cliente que comprou há 40 dias cai em qual regra?

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco":
    do time("televendas")
    quando recencia de positivacao entre 31 dias e 60 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 28 dias
```

Um cliente que comprou há 40 dias cai na regra "Risco", pois a regra "Ativos" captura apenas até 30 dias, e a regra "Risco" captura de 31 a 60 dias.

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 40.

**Verificações:**
- [ ] arquivo do turno 1
- [x] resposta tem Risco

## Turno 3 (inicial, 31 s, 4741 tokens no maior prompt)

**Usuário:** E um que está sem comprar há 100 dias, é agendado de quanto em quanto tempo?

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco":
    do time("televendas")
    quando recencia de positivacao entre 31 dias e 60 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 60 dias
    frequencia de 28 dias
```

Um cliente que comprou há 40 dias cai na regra "Risco".
Um cliente sem comprar há 100 dias é agendado a cada 28 dias.

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 40, 100.

**Verificações:**
- [ ] arquivo do turno 1
- [x] resposta tem 28
