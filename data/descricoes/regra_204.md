# regra_204.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas de frequência. Antes das faixas, deixam de ser agendados os clientes que compraram nos últimos 7 dias. A última faixa atende os clientes inativos, incluindo os que nunca compraram.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra nos últimos 7 dias | Clientes que compraram nos últimos 7 dias | Não agendar |  |
| Regularidade de compra | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Positivação da carteira | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Inativos | Clientes que nunca compraram ou estão há mais de 90 dias sem comprar | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |
