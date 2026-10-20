# regra_218.gobr

Regras de frequência para dois times de televendas: televendas_1 e televendas_2. O primeiro time organiza os clientes por tempo desde a última compra (mais de 7 dias, últimos 7 dias e quem nunca comprou). O segundo organiza por compra no grupo de vendedores em 30 dias e pela relação com o próprio vendedor. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem compra há mais de 7 dias | Clientes que estão há mais de 7 dias sem comprar | 5 dias | Time televendas_1 |
| Compra recente | Clientes que compraram nos últimos 7 dias, exceto os já tratados pela regra anterior | Pelo histórico de compras | Sem histórico, limitada a no máximo 14 dias. Time televendas_1 |
| Nunca compraram | Clientes que nunca compraram | 14 dias | Time televendas_1 |
| Sem pedido com o vendedor | Clientes que nunca compraram com o próprio vendedor | 14 dias | Time televendas_2 |
| Compra em 30 dias | Clientes que compraram no grupo de vendedores nos últimos 30 dias e já compraram com o próprio vendedor | 14 dias | Time televendas_2 |
| Sem compra há mais de 30 dias | Clientes que estão há mais de 30 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Time televendas_2 |
