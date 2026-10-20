# regra_243.gobr

Regra de planejamento do time de televendas voltada a clientes pessoa jurídica: novos clientes a cada 21 dias, pós-vendas a cada 3 dias e clientes engajados pelo histórico de visitas. O atendimento tem preferência de segunda a sábado. Deixam de ser agendados os clientes sem compra recente e os que não são pessoa jurídica.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ative este cliente | Clientes pessoa jurídica sem vendas para o vendedor | 21 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Pós-vendas | Clientes pessoa jurídica com venda para o vendedor que compraram nos últimos 20 dias | 3 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Cliente engajado | Clientes pessoa jurídica com venda para o vendedor que compraram nos últimos 33 dias, mas estão há mais de 20 dias sem comprar | Pelo histórico mais 2 dias, entre 20 e 33 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Bloqueio: sem compra em 33 dias | Clientes pessoa jurídica com venda para o vendedor que nunca compraram ou estão há mais de 33 dias sem comprar | Não agendar |  |
| Bloqueio: não é PJ | Clientes pessoa física ou sem tipo de pessoa definido | Não agendar |  |

## Pontos de atenção

- O bloqueio 'Não agendar clientes sem compra em 33 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram nelas.
