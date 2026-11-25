# muda_criterio

## Turno 1 (inicial, 24 s, 4750 tokens no maior prompt)

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

## Turno 2 (alterar, 28 s, 5326 tokens no maior prompt)

**Usuário:** O corte entre ativo e inativo passa a ser de 45 dias sem compra, as frequências continuam.

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
    quando inatividade de 45 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 30 dias, 28 dias" para "Inativos: sem compra há mais de 45 dias, 28 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `inatividade de 30 dias`, entrou `inatividade de 45 dias`

**Verificações:**
- [ ] Ativos: {"dias": 14, "numero": 45}
- [x] Inativos: {"dias": 28}
- [ ] sem o 30
