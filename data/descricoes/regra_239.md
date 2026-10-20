# regra_239.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas (até 60, 90, 120, 150 e 180 dias, sendo a primeira para clientes ativos). Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal e os que têm rota do vendedor externo na semana. Quem não se enquadra em nenhuma faixa também não é agendado.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: rota do externo na semana | Clientes com data de rota do vendedor externo nesta semana | Não agendar |  |
| Clientes ativos | Clientes que compraram nos últimos 60 dias | 14 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Inativos (90 dias) | Clientes que compraram nos últimos 120 dias, mas estão há mais de 90 dias sem comprar | 14 dias |  |
| Inativos (120 dias) | Clientes que compraram nos últimos 150 dias, mas estão há mais de 120 dias sem comprar | 21 dias |  |
| Inativos (150 dias) | Clientes que compraram nos últimos 180 dias, mas estão há mais de 150 dias sem comprar | 28 dias |  |
| Bloqueio: clientes não mapeados | Clientes que nunca compraram ou estão há mais de 180 dias sem comprar | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |
