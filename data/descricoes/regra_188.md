# regra_188.gobr

Regra de agendamento do time televendas por tempo sem comprar com o vendedor. Antes das faixas, deixam de ser agendados os inadimplentes, as filiais e os baixados na Receita Federal. Em seguida vêm os clientes sem vendas para o vendedor, a compra regular, as faixas de clientes parando de comprar e, por último, os que nunca compraram mas têm alguma venda para o vendedor.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Pré-qualificados sem vendas | Clientes sem vendas para o vendedor | 21 dias |  |
| Compra regular | Clientes que compraram nos últimos 30 dias e têm alguma venda (ativos ou inativos) para o vendedor | Pelo histórico, entre 7 e 30 dias |  |
| Estimular regularidade | Clientes que estão há mais de 45 dias sem comprar e têm alguma venda (ativos ou inativos) para o vendedor | 14 dias |  |
| Deixando de comprar | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias |  |
| Resgate | Clientes que nunca compraram, mas têm alguma venda (ativos ou inativos) para o vendedor | 14 dias |  |
