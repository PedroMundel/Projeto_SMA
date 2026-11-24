# lembra_resposta

## Turno 1 (inicial, 48 s, 12889 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

parametros "Ativos":
    do time("padrao")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Os inativos a cada 28 dias.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 95 s, 15428 tokens no maior prompt)

**Usuário:** Mude os ativos para 7 dias.

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

parametros "Ativos":
    do time("padrao")
    quando atividade de 30 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 7 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 7 dias`

**Verificações:**
- [x] Ativos: {"dias": 7}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] até 0 perguntas
