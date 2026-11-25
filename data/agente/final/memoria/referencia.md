# referencia

## Turno 1 (inicial, 24 s, 4764 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 90 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 90 dias
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28, "numero": 90}

## Turno 2 (duvida, 8 s, 1779 tokens no maior prompt)

**Usuário:** A partir de quantos dias sem comprar o cliente conta como inativo?

**Agente:**

Na regra atual, um cliente é considerado inativo se não comprar há pelo menos 90 dias. Isso está definido no filtro "inatividade de 90 dias" da regra "Inativos".

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem 90

## Turno 3 (alterar, 27 s, 4690 tokens no maior prompt)

**Usuário:** Aumente esse prazo para 120.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 120 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 90 dias, 28 dias" para "Inativos: sem compra há mais de 120 dias, 28 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `inatividade de 90 dias`, entrou `inatividade de 120 dias`

**Verificações:**
- [x] Inativos: {"dias": 28, "numero": 120}
- [x] Ativos intacta
- [x] sem o 90
