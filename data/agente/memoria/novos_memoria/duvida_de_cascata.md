# duvida_de_cascata

## Turno 1 (inicial, 26 s, 4736 tokens no maior prompt)

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

## Turno 2 (duvida, 10 s, 1596 tokens no maior prompt)

**Usuário:** Um cliente que comprou há 40 dias cai em qual regra?

**Agente:**

Ele cai na regra "Risco".
A regra "Ativos" exige compra nos últimos 30 dias (40 dias não se encaixa).
A regra "Risco" captura quem comprou nos últimos 60 dias, mas está há mais de 30 dias sem comprar.
Como 40 dias está entre 30 e 60 dias, o cliente é elegível para esta regra.
A regra "Inativos" só pega quem está há mais de 60 dias.
Portanto, a primeira regra aplicável é "Risco".

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem Risco

## Turno 3 (duvida, 10 s, 2262 tokens no maior prompt)

**Usuário:** E um que está sem comprar há 100 dias, é agendado de quanto em quanto tempo?

**Agente:**

Ele cai na regra "Inativos", pois está sem compra há mais de 60 dias.
A regra "Ativos" exige compra nos últimos 30 dias (100 dias não se encaixa).
A regra "Risco" captura quem comprou nos últimos 60 dias (100 dias ultrapassa esse limite).
A regra "Inativos" aplica-se a quem está sem comprar há mais de 60 dias.
Portanto, a frequência de agendamento é de 28 dias.

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem 28
