# regra_212.gobr

Regra de agendamento do time televendas por tempo desde a última compra, em faixas de até 30, 60, 90, 180 e 360 dias, mais os clientes que nunca compraram. Deixam de ser agendados os clientes com rota nos próximos 7 dias e os que compraram com a empresa nos últimos 14 dias. A regra final atende, a cada 7 dias, quem não se enquadrou nas anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: rota nos próximos 7 dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Bloqueio: compra nos últimos 14 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias | Não agendar |  |
| Regularidade de compra | Clientes que compraram nos últimos 30 dias, mas estão há mais de 14 dias sem comprar, com data de rota há 7 dias e visita na semana anterior | 7 dias |  |
| Último pedido entre 30 e 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com data de rota há 7 dias e visita na semana anterior | 20 dias |  |
| Ativar: sem pedidos | Clientes sem vendas para o vendedor que nunca compraram na empresa ou estão há mais de 14 dias sem comprar | 14 dias | Com rota há 7 dias e visita na semana anterior, vale após mais de 60 dias sem comprar |
| Ativar: inativos | Clientes que compraram nos últimos 360 dias, mas estão há pelo menos 180 dias sem comprar, com compra no ano anterior e alguma venda para o vendedor | 14 dias |  |
| Caminhando para inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, com alguma venda para o vendedor | 7 dias |  |
| Resgate: último pedido entre 90 e 180 dias | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, com alguma venda para o vendedor | 7 dias | Quem comprou no ano anterior entra se comprou nos últimos 179 dias |
| Demais clientes | Clientes do time televendas sem outro enquadramento, exceto os já tratados pelas regras anteriores | 7 dias | Regra final: vale para quem sobrou das anteriores |

## Pontos de atenção

- A regra 'Atendimento ao cliente que não se enquadrou nas demais regras' é descrita pela condição própria, exceto os clientes já tratados pelas regras anteriores, porque a condição efetiva é fragmentada demais para resumir.
