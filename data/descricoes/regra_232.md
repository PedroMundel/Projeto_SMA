# regra_232.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em faixas de 29, 59 e 89 dias, mais os prospects e os clientes que compraram na empresa mas não no grupo de vendedores. Deixam de ser agendadas as filiais e os clientes inadimplentes. A última regra atende quem sobrou das faixas anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Compra entre 1 e 29 dias | Clientes que compraram nos últimos 29 dias | Pelo histórico de compras; sem histórico, entre 14 e 30 dias |  |
| Compra entre 30 e 59 dias | Clientes que compraram nos últimos 59 dias, mas estão há mais de 29 dias sem comprar | 21 dias |  |
| Compra entre 60 e 89 dias | Clientes que compraram nos últimos 89 dias, mas estão há mais de 59 dias sem comprar | 21 dias |  |
| Sem compra em 90 dias | Clientes que já compraram com qualquer vendedor da empresa, mas nunca compraram no grupo de vendedores ou estão há mais de 89 dias sem comprar nele | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |
