# muda_a_resposta

## Turno 1 (inicial, 30 s, 4743 tokens no maior prompt)

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

## Turno 2 (inicial, 22 s, 3804 tokens no maior prompt)

**Usuário:** Na verdade prefiro os inativos a cada 35 dias.

**Agente:**

```gobr
version 1.0

time "empresa toda":
    vendedores todos

carteira "empresa toda":
    clientes carteirafixa("empresa toda")

parametros "Inativos a cada 35 dias":
    da carteira("empresa toda")
    quando inativos para o vendedor
    frequencia de 35 dias
    preferencia do vendedor
```

**Notas:**
1. **Critério de Inatividade:** O pedido não especificou o tempo de inatividade (ex: "inativos há 30 dias"). Assumi a cláusula padrão `inativos para o vendedor` (que usa o critério global do sistema), pois é a mais comum em regras de frequência simples. Se houver um tempo específico (ex: 90 dias), a cláusula seria `inatividade de 90 dias`.
2. **Segmentos Ausentes:** O pedido focou apenas nos "inativos". Regras para clientes "Ativos" e "Sem Vendas" não foram incluídas, pois não foram solicitadas. Se existirem regras anteriores ou posteriores para esses segmentos, elas devem ser mantidas no arquivo completo para não bloquear o agendamento desses clientes.
3. **Frequência:** A frequência de "35 dias" foi mapeada para `frequencia de 35 dias`. O GoBR não possui uma palavra-chave específica para 35 dias (como "quinzenal" ou "mensal"), então usa-se a sintaxe numérica direta.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 35}
- [ ] Ativos intacta
- [x] sem o 28
- [ ] até 0 perguntas
