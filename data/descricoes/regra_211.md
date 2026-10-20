# regra_211.gobr

Regra de agendamento do time de ativação, formado pelos vendedores de id 965 e 945, em duas faixas conforme haja ou não pedido nos últimos 30 dias. Quem comprou nos últimos 30 dias tem frequência de 21 dias; os demais, de 15 dias. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Com pedido nos últimos 30 dias | Clientes que compraram nos últimos 30 dias | 21 dias |  |
| Sem pedido nos últimos 30 dias | Clientes que nunca compraram ou estão há mais de 30 dias sem comprar | 15 dias |  |
