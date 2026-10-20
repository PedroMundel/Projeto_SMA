# regra_184.gobr

Regra de agendamento com dois times. O televendas é organizado pelo tempo desde a última compra, em faixas de até 7, 14, 30, 90 e 180 dias e acima de 360 dias, com tratamento próprio para quem fez uma única compra no mês atual. O time São Paulo segue frequências fixas conforme a frequência histórica de compra, com preferência pela segunda. Não há bloqueios, e a regra final cobre os demais clientes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Recorrência de compra | Clientes com compra no mês atual e com uma única compra na empresa | 5 dias |  |
| Alta frequência de compra | Clientes que compraram nos últimos 7 dias, mas estão há pelo menos 1 dia sem comprar | Pelo histórico, entre 1 e 5 dias | Dias de preferência: segunda e terça; demais dias sem atendimento |
| Regularidade de compra | Clientes que compraram nos últimos 14 dias, mas estão há mais de 7 dias sem comprar | Pelo histórico, entre 7 e 12 dias |  |
| Estímulo dentro do mês | Clientes que compraram nos últimos 30 dias, mas estão há mais de 14 dias sem comprar | Pelo histórico, entre 14 e 28 dias |  |
| Relacionamento e estímulo | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar | 14 dias |  |
| Resgate de inativos | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 14 dias |  |
| Requalificação | Clientes que estão há mais de 360 dias sem comprar | 21 dias |  |
| Frequência semanal (São Paulo) | Clientes do time São Paulo com frequência histórica de compra de 7 dias | 7 dias | Maior preferência na segunda; demais dias sem atendimento; frequência e dias fixos para o gerador de agendas |
| Frequência quinzenal (São Paulo) | Clientes do time São Paulo com frequência histórica de compra de 14 dias | 14 dias | Maior preferência na segunda; demais dias sem atendimento; frequência e dias fixos para o gerador de agendas |
| Frequência mensal (São Paulo) | Clientes do time São Paulo com frequência histórica de compra de 28 dias | 28 dias | Maior preferência na segunda; demais dias sem atendimento; frequência e dias fixos para o gerador de agendas |
| Frequência bimestral (São Paulo) | Clientes do time São Paulo com frequência histórica de compra de 56 dias | 56 dias | Maior preferência na segunda; demais dias sem atendimento; frequência e dias fixos para o gerador de agendas |
| Frequência trimestral (São Paulo) | Clientes do time São Paulo com frequência histórica de compra de 84 dias | 84 dias | Maior preferência na segunda; demais dias sem atendimento; frequência e dias fixos para o gerador de agendas |
| Demais clientes | Clientes do time São Paulo fora das frequências históricas fixas e do televendas que nunca compraram, compraram hoje ou estão há mais de 180 e até 360 dias sem comprar | 30 dias | Regra final: vale para quem sobrou das faixas anteriores |
