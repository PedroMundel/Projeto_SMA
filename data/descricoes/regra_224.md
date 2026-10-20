# regra_224.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro grupos: prospects, ativos, risco de inatividade e inativos há mais de 90 dias. Antes deles, deixam de ser agendados os clientes baixados na Receita Federal e os que têm rota do vendedor externo na semana. A última faixa atende quem está há mais de 90 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: rota do externo na semana | Clientes com data de rota do vendedor externo nesta semana | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Clientes ativos | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 7 dias |  |
| Risco de inatividade | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Inativos há mais de 90 dias | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
