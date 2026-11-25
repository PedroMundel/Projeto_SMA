# muda_so_o_criterio

## Turno 1 (inicial, 26 s, 4277 tokens no maior prompt)

**Usuário:** Recorrentes: compra nos últimos 30 dias, 14 dias
Parados: sem compra há mais de 30 dias, 35 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Recorrentes":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Parados":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 35 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Recorrentes: {"dias": 14}
- [x] Parados: {"dias": 35}

## Turno 2 (alterar, 31 s, 4992 tokens no maior prompt)

**Usuário:** Considere parado só quem não compra há mais de 75 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Recorrentes":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Parados":
    do time("televendas")
    quando inatividade de 75 dias
    frequencia de 35 dias
```

Mudança no pedido:
- de "Parados: sem compra há mais de 30 dias, 35 dias" para "Parados: sem compra há mais de 75 dias, 35 dias"

O que mudou no arquivo:
- "Parados" (parametros): saiu `inatividade de 30 dias`, entrou `inatividade de 75 dias`

- "Parados: sem compra há mais de 75 dias": alterado de 30 para 75 dias na cláusula `inatividade de 75 dias`.
- Premissa assumida: a ordem das regras mantém "Recorrentes" antes de "Parados", o que é correto pois um cliente com compra nos últimos 30 dias não terá inatividade de 75 dias.
- Não há pontos falhos ou trechos não suportados no GoBR para esta alteração específica.

**Verificações:**
- [x] Parados: {"dias": 35, "numero": 75}
- [x] Recorrentes: {"dias": 14}
- [x] Recorrentes intacta
