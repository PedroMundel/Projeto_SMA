# regra_157.gobr

Regra padrão do time toda empresa, com frequência de visita definida pelo tempo desde a última compra, em três faixas. Quem está há mais de 120 dias sem comprar é atendido a cada 14 dias, quem comprou nos últimos 120 dias mas está há mais de 30 dias parado a cada 7 dias, e os demais pelo histórico. O atendimento é de segunda a sexta, e nenhuma regra bloqueia a agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Mais de 120 dias sem vendas | Clientes que estão há mais de 120 dias sem comprar | 14 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Mais de 30 dias sem vendas | Clientes que compraram nos últimos 120 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Prospects e compradores recentes | Clientes que nunca compraram ou compraram nos últimos 30 dias | Pelo histórico, entre 5 e 30 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
