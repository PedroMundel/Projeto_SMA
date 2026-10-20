# regra_212.gobr

Regra de agendamento do time de televendas por tempo desde a última compra na empresa, rota do vendedor externo e visita na semana anterior, com faixas de 7, 14 e 20 dias. Deixam de ser agendados os clientes com rota nos próximos 7 dias e os que compraram nos últimos 14 dias. A regra final atende todos os clientes que sobraram das faixas anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: rota nos próximos 7 dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Bloqueio: compra nos últimos 14 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias | Não agendar |  |
| Regularidade (pedido em até 30 dias) | Clientes que compraram na empresa nos últimos 30 dias, estão há mais de 14 dias sem comprar, com data de rota há 7 dias e visita na semana anterior | 7 dias |  |
| Último pedido entre 30 e 60 dias | Clientes que compraram na empresa nos últimos 60 dias, estão há mais de 30 dias sem comprar, com data de rota há 7 dias e visita na semana anterior | 20 dias |  |
| Ativação de clientes sem vendas | Clientes sem vendas para o vendedor que nunca compraram na empresa ou estão há mais de 14 dias sem comprar (mais de 60 dias com rota há 7 dias e visita na semana anterior) | 14 dias |  |
| Ativação de clientes antigos | Clientes que compraram na empresa nos últimos 360 dias, estão há pelo menos 180 dias sem comprar, compraram no ano anterior e têm alguma venda para o vendedor | 14 dias |  |
| Caminhando para inatividade | Clientes que compraram na empresa nos últimos 90 dias, estão há mais de 60 dias sem comprar e têm alguma venda para o vendedor | 7 dias |  |
| Resgate (90 a 180 dias) | Clientes que compraram na empresa nos últimos 180 dias, estão há mais de 90 dias sem comprar e têm alguma venda para o vendedor | 7 dias | Quem comprou no ano anterior entra se comprou nos últimos 179 dias |
| Demais clientes | Todos os clientes do time, exceto os já tratados pelas regras anteriores | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A condição da regra 'Atendimento ao cliente que não se enquadrou nas demais regras.' é fragmentada demais para resumir: ela vale para todos os clientes do time, exceto os já tratados pelas regras anteriores.
