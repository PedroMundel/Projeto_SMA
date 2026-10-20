# regra_188.gobr

Regra de agendamento do time televendas por situação de compra do cliente com o vendedor. Não são agendados os inadimplentes, as filiais e os baixados na Receita Federal. Os demais são separados em sem vendas para o vendedor, compra regular nos últimos 30 dias, faixas de tempo sem comprar (mais de 30 e mais de 45 dias) e quem nunca comprou.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Pré-qualificados sem vendas | Clientes sem vendas para o vendedor | 21 dias |  |
| Compra regular | Clientes que compraram nos últimos 30 dias e têm alguma venda (ativos ou inativos) para o vendedor | Pelo histórico, entre 7 e 30 dias |  |
| Estimular regularidade | Clientes que estão há mais de 45 dias sem comprar e têm alguma venda (ativos ou inativos) para o vendedor | 14 dias |  |
| Deixando de comprar | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar, e têm alguma venda (ativos ou inativos) para o vendedor | 7 dias |  |
| Resgate de perfil | Clientes que nunca compraram e têm alguma venda (ativos ou inativos) para o vendedor | 14 dias |  |
