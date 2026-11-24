# mudanca_global

## Turno 1 (inicial, 21 s, 4787 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 45 dias, 14 dias
Inativos: sem compra há mais de 45 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao global em 45 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao global em 45 dias
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 26 s, 4561 tokens no maior prompt)

**Usuário:** Quero todos os segmentos com a mesma frequência, a cada 10 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao global em 45 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao global em 45 dias
    frequencia de 10 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 45 dias, 14 dias" para "Ativos: compra nos últimos 45 dias, 10 dias"
- de "Inativos: sem compra há mais de 45 dias, 28 dias" para "Inativos: sem compra há mais de 45 dias, 10 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 10 dias`
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 10 dias`

**Verificações:**
- [x] Ativos: {"dias": 10, "numero": 45}
- [x] Inativos: {"dias": 10}
- [x] sem o 14
- [x] sem o 28
