# regra_197.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas: prospects, ativos (até 60 dias), risco de inatividade (até 90 dias) e inativos há mais de 90 dias. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal, os inadimplentes e os que têm rota do vendedor externo na semana. A última faixa atende os inativos há mais de 90 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: rota do externo na semana | Clientes com data de rota do vendedor externo nesta semana | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Clientes ativos | Clientes que compraram na empresa nos últimos 60 dias | 7 dias |  |
| Risco de inatividade | Clientes que compraram na empresa nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Inativos (mais de 90 dias) | Clientes que estão há mais de 90 dias sem comprar na empresa | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |
