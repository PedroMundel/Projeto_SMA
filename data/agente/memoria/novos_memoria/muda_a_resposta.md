# muda_a_resposta

## Turno 1 (inicial, 28 s, 4743 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando nao tem venda em 60 dias
    frequencia de 28 dias
```

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Agendar os inativos a cada 28 dias.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 27 s, 4280 tokens no maior prompt)

**Usuário:** Na verdade prefiro os inativos a cada 35 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando nao tem venda em 60 dias
    frequencia de 35 dias
```

Mudança no pedido:
- de "Resposta do usuário (Para escrever as regras sem chutar, faltam estes dados no pedido: - "Inativos": agendar ou não agendar? Responda numa mensagem só.): Agendar os inativos a cada 28 dias." para "Pedido do usuário (Para escrever as regras sem chutar, faltam estes dados no pedido: - "Inativos": agendar ou não agendar? Responda numa mensagem só.): Agendar os inativos a cada 35 dias."

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 35 dias`

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 35}
- [x] Ativos intacta
- [x] sem o 28
- [x] até 0 perguntas
