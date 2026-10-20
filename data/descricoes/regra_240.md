# regra_240.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas (até 30, 60 e 90 dias e acima de 90 dias, incluindo quem nunca comprou). Antes das faixas, deixam de ser agendados os clientes que compraram nos últimos 7 dias. A última faixa cobre todos os clientes que sobram das anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra nos últimos 7 dias | Clientes que compraram nos últimos 7 dias | Não agendar |  |
| Compra regular | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Positivação da carteira | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Clientes inativos | Clientes que nunca compraram ou estão há mais de 90 dias sem comprar | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |
