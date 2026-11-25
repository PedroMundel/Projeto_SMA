```gobr
version 1.0

time "todos os vendedores":
    vendedores todos ativados

parametros "Clientes Inadimplentes":
    da time("todos os vendedores")
    quando inadimplentes
    nao agendar

parametros "O resto (ativo, inativo, prospect) adimplente":
    da time("todos os vendedores")
    quando adimplentes
    frequencia de 7 dias
```

**Observações:**
1. **Segmentação de Clientes:** O pedido menciona "ativo, inativo, prospect". Como não há distinção de frequência para esses grupos no pedido (todos "adimplente a cada 7 dias"), uma única regra para `adimplentes` cobre todos eles, pois a regra de inadimplentes (`nao agendar`) roda primeiro e bloqueia os inadimplentes.
2. **Ordem das Regras:** A regra de bloqueio ("Clientes Inadimplentes") foi colocada primeiro. No GoBR, a primeira regra que se aplica vence. Isso garante que um cliente inadimplente não caia na regra de agendamento de 7 dias.
3. **Cláusula `quando`:** Utilizei `quando inadimplentes` e `quando adimplentes` baseando-me nos exemplos fornecidos (ex: regra_075, regra_105), onde a situação financeira é um filtro direto.
4. **Fidelidade:** Todos os números (7 dias) e ações (nao agendar, frequencia) do pedido foram respeitados. Não há cláusulas inventadas.