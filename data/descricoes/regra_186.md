# regra_186.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, com clientes sem vendas, clientes reativados e faixas de relacionamento de 7 dias. Antes das faixas, não são agendados os clientes que compraram com o televendas nos últimos 7 dias nem os que têm rota nos próximos 7 dias. A regra final atende os demais clientes a cada 28 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra recente | Clientes que compraram com o próprio vendedor nos últimos 7 dias | Não agendar |  |
| Bloqueio: rota nos próximos dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Nunca tirou pedido | Clientes sem vendas para a empresa | 14 dias |  |
| Ativar cliente | Clientes que compraram nos últimos 360 dias, mas estão há pelo menos 180 dias sem comprar, com compra no ano anterior e alguma venda para a empresa | 14 dias |  |
| Cliente reativado | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias, com compra anterior na empresa entre 181 e 360 dias atrás e sem compra entre 15 e 180 dias atrás | 14 dias |  |
| Regularidade de compra (7 a 30 dias) | Clientes com compra na empresa entre 7 e 30 dias atrás, data de rota há 7 dias e visita na semana anterior, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Regularidade de compra (31 a 60 dias) | Clientes com compra na empresa entre 31 e 60 dias atrás, data de rota há 7 dias e visita na semana anterior, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Caminhando para inatividade | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Resgate de clientes | Clientes que compraram com qualquer vendedor da empresa nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Demais clientes | Todos os clientes do time, exceto os já tratados pelas regras anteriores | 28 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A sequência de regras mistura recortes de tempo sem compra diferentes (da empresa toda, do grupo de vendedores e do próprio vendedor); as faixas não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
