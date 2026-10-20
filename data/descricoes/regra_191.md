# regra_191.gobr

Regra de agendamento do time televendas por tempo desde a última compra, com prospects, pós-venda, faixas até 30, 45 e 60 dias e os inativos. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal e os inadimplentes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Pós-venda | Clientes que compraram nos últimos 7 dias | 21 dias |  |
| Alta regularidade | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | Pelo histórico mais 3 dias, entre 14 e 30 dias |  |
| Estimular regularidade | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 60 dias, mas estão há mais de 45 dias sem comprar | 7 dias |  |
| Inativos | Clientes que já compraram na empresa, mas nunca compraram no grupo de vendedores ou estão há mais de 60 dias sem comprar nele | 7 dias |  |
