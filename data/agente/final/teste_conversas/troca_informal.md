# troca_informal

## Turno 1 (inicial, 29 s, 4867 tokens no maior prompt)

**Usuário:** Frequentes: compra nos últimos 40 dias, 10 dias
Sumidos: sem compra há mais de 40 dias, 25 dias

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Frequentes":
    do time("televendas")
    quando recencia de positivacao em 40 dias
    frequencia de 10 dias

parametros "Sumidos":
    do time("televendas")
    quando inatividade de 40 dias
    frequencia de 25 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Frequentes: {"dias": 10}
- [x] Sumidos: {"dias": 25}

## Turno 2 (alterar, 30 s, 5045 tokens no maior prompt)

**Usuário:** bota os sumidos de 18 em 18

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Frequentes":
    do time("televendas")
    quando recencia de positivacao em 40 dias
    frequencia de 10 dias

parametros "Sumidos":
    do time("televendas")
    quando inatividade de 40 dias
    frequencia de 18 dias
```

Mudança no pedido:
- de "Sumidos: sem compra há mais de 40 dias, 25 dias" para "Sumidos: sem compra há mais de 40 dias, 18 dias"

O que mudou no arquivo:
- "Sumidos" (parametros): saiu `frequencia de 25 dias`, entrou `frequencia de 18 dias`

**Verificações:**
- [x] Sumidos: {"dias": 18, "numero": 40}
- [x] Frequentes: {"dias": 10}
- [x] Frequentes intacta
- [x] sem o 25
