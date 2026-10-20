# regra_223.gobr

Regras de frequência para três times: ativação, generalista e construtora. O time de ativação usa duas faixas conforme o cliente comprou ou não nos últimos 30 dias (21 e 15 dias). O time generalista não agenda clientes com compra na semana atual e atende os demais a cada 7 dias. O time construtora atende todos os clientes a cada 14 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativação: com pedido em 30 dias | Clientes que compraram nos últimos 30 dias | 21 dias | Time ativação |
| Ativação: sem pedido em 30 dias | Clientes que nunca compraram ou estão há mais de 30 dias sem comprar | 15 dias | Time ativação |
| Bloqueio: compra na semana | Clientes com compra na semana atual | Não agendar | Time generalista |
| Generalista: cliente semanal | Clientes de todo o time generalista, sem filtro de compra | 7 dias | Time generalista |
| Construtora: todos os clientes | Clientes de todo o time construtora, sem filtro de compra | 14 dias | Time construtora |
