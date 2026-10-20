# regra_238.gobr

Regra de agendamento do time de televendas por tempo desde a última compra com qualquer vendedor da empresa, em três faixas (até 59, até 89 e acima de 89 dias, incluindo quem nunca comprou). Todas as faixas usam frequência de 14 dias. Não há regras de bloqueio, e a última faixa cobre todos os clientes que sobram das anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Clientes ativos | Clientes que compraram com qualquer vendedor da empresa nos últimos 59 dias | 14 dias |  |
| Risco de inatividade | Clientes que compraram com qualquer vendedor da empresa nos últimos 89 dias, mas estão há mais de 59 dias sem comprar | 14 dias |  |
| Clientes inativos | Clientes que nunca compraram com qualquer vendedor da empresa ou estão há mais de 89 dias sem comprar | 14 dias | Regra final: vale para quem sobrou das faixas anteriores |
