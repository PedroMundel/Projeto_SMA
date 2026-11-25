# lembra_resposta

## Turno 1 (inicial, 31 s, 5405 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda do vendedor em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inativos para o vendedor
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Os inativos a cada 28 dias.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 27 s, 4536 tokens no maior prompt)

**Usuário:** Mude os ativos para 7 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda do vendedor em 30 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    quando inativos para o vendedor
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
