# regra_152.gobr

Regra de agendamento do time de televendas por histórico de compra com o próprio vendedor e por tempo desde a última compra no grupo de vendedores, em faixas de 7, 30, 60 e 90 dias. Prospects e clientes com uma única compra com o vendedor são atendidos a cada 7 dias. Não há regras de bloqueio. A última regra atende quem está há mais de 90 dias sem comprar no grupo.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Primeiro pedido | Clientes que já compraram com o próprio vendedor, mas em uma única compra | 7 dias |  |
| Pedido entre 0 e 7 dias | Clientes que compraram no grupo de vendedores nos últimos 7 dias e têm mais de uma compra com o próprio vendedor | 14 dias |  |
| Pedido entre 7 e 30 dias | Clientes que compraram no grupo nos últimos 30 dias, mas estão há mais de 7 dias sem comprar, com mais de uma compra com o próprio vendedor | 14 dias |  |
| Pedido entre 30 e 60 dias | Clientes que compraram no grupo nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com mais de uma compra com o próprio vendedor | 14 dias |  |
| Pedido entre 60 e 90 dias | Clientes que compraram no grupo nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra com o próprio vendedor | 7 dias |  |
| Pedido há 90 dias ou mais | Clientes que estão há mais de 90 dias sem comprar no grupo de vendedores, com mais de uma compra com o próprio vendedor | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |
