# regra_232.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, com os prospects e quatro faixas de recência. Deixam de ser agendadas as filiais e os clientes inadimplentes. A faixa final cobre quem está há mais de 89 dias sem comprar no grupo de vendedores, com frequência de 21 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Compra entre 1 e 29 dias | Clientes que compraram nos últimos 29 dias | Pelo histórico, entre 14 e 30 dias |  |
| Compra entre 30 e 59 dias | Clientes que compraram nos últimos 59 dias, mas estão há mais de 29 dias sem comprar | 21 dias |  |
| Compra entre 60 e 89 dias | Clientes que compraram nos últimos 89 dias, mas estão há mais de 59 dias sem comprar | 21 dias |  |
| Sem compra em 90 dias | Clientes sem comprar no grupo de vendedores há mais de 89 dias ou que só compraram com vendedores de outros grupos | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |
