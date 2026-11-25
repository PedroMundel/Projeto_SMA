# muda_a_resposta

## Turno 1 (inicial, 32 s, 4856 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Agendar os inativos a cada 28 dias.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 58 s, 11337 tokens no maior prompt)

**Usuário:** Na verdade prefiro os inativos a cada 35 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 35 dias
```

Mudança no pedido:
- de "Resposta do usuário (Para escrever as regras sem chutar, faltam estes dados no pedido: - "Inativos": agendar ou não agendar? Responda numa mensagem só.): Agendar os inativos a cada 28 dias." para "Pedido do usuário (Para escrever as regras sem chutar, faltam estes dados no pedido: - "Inativos": agendar ou não agendar? Responda numa mensagem só.): Agendar os inativos a cada 35 dias."

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `fora da recencia de positivacao em 60 dias`; `frequencia de 35 dias`

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 35}
- [x] Ativos intacta
- [x] sem o 28
- [x] até 0 perguntas
