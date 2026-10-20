# regra_218.gobr

Regra de agendamento com dois times de televendas: televendas_1 (todos os vendedores habilitados, exceto os de id 4504) e televendas_2 (os vendedores de id 4504). O primeiro time organiza os clientes por tempo sem comprar, com frequência de 5 dias, pelo histórico ou de 14 dias; o segundo, por compra com o próprio vendedor e no grupo de vendedores. Não há bloqueios nem carteiras.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem compra há mais de 7 dias | Clientes que estão há mais de 7 dias sem comprar | 5 dias | Time televendas_1 |
| Compra recente | Clientes que compraram nos últimos 7 dias | Pelo histórico, no máximo 14 dias | Time televendas_1 |
| Sem compra | Clientes que nunca compraram | 14 dias | Time televendas_1 |
| Sem pedido | Clientes que nunca compraram com o próprio vendedor | 14 dias | Time televendas_2 |
| Com compra em 30 dias | Clientes que compraram no grupo de vendedores nos últimos 30 dias e já compraram com o próprio vendedor | 14 dias | Time televendas_2 |
| Sem compra há mais de 30 dias | Clientes que estão há mais de 30 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Time televendas_2 |
