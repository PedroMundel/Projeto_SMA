# regra_157.gobr

Regra padrão de frequência aplicada ao time de todos os vendedores habilitados, com atendimento preferencial de segunda a sexta. Clientes há mais de 120 dias sem comprar são atendidos a cada 14 dias, e os que estão entre 30 e 120 dias sem comprar, a cada 7 dias. A regra final cobre quem nunca comprou ou comprou nos últimos 30 dias, com frequência pelo histórico de compras. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Mais de 120 dias sem vendas | Clientes que estão há mais de 120 dias sem comprar | 14 dias | Dias de preferência: segunda a sexta |
| Mais de 30 dias sem vendas | Clientes que compraram nos últimos 120 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Dias de preferência: segunda a sexta |
| Nunca compraram ou compra recente | Clientes que nunca compraram ou compraram nos últimos 30 dias | Pelo histórico, entre 5 e 30 dias | Regra final; se não houver histórico, frequência limitada a no mínimo 5 e no máximo 30 dias. Preferência: segunda a sexta |
