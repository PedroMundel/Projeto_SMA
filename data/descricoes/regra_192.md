# regra_192.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas: prospects, ativos, risco de inatividade e inativos. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal. A faixa de inativos é a final e trata quem sobrou das anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Clientes ativos | Clientes que compraram nos últimos 15 dias | 7 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 30 dias, mas estão há mais de 15 dias sem comprar | 3 dias |  |
| Inativos (30 dias) | Clientes que já compraram na empresa, mas nunca compraram no grupo de vendedores ou estão há mais de 30 dias sem comprar nele | 5 dias | Regra final: vale para quem sobrou das faixas anteriores |
