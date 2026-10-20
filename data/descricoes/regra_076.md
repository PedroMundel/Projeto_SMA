# regra_076.gobr

Agendamento do time de televendas por rota e por tempo desde a última compra. Não são agendados os inadimplentes, os bloqueados para atendimento, os inativos para a empresa e quem comprou nos últimos 20 dias. Clientes com data de rota hoje têm frequência de 1 dia; os demais seguem faixas para prospects, cliente ativado, quem compra regularmente e quem está em ruptura. A regra final bloqueia os clientes fora de rota que não entraram em nenhuma faixa.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: inativos | Clientes inativos para a empresa | Não agendar |  |
| Bloqueio: compra recente | Clientes que compraram com qualquer vendedor da empresa nos últimos 20 dias | Não agendar |  |
| Clientes com rota hoje | Clientes com data de rota hoje que nunca compraram ou estão há mais de 20 dias sem comprar | 1 dia |  |
| Prospects | Clientes que nunca compraram na empresa e não têm data de rota hoje | 7 dias |  |
| Cliente ativado | Clientes com uma única compra na empresa, há mais de 20 dias sem comprar e sem data de rota hoje | 15 dias |  |
| Compra regularmente | Clientes com mais de uma compra, que compraram nos últimos 30 dias, mas estão há mais de 20 dias sem comprar, sem rota hoje e com frequência histórica de compra de menos de 30 dias | Pelo histórico, entre 5 e 30 dias |  |
| Em ruptura | Clientes com mais de uma compra, que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar e sem data de rota hoje | 15 dias |  |
| Bloqueio: fora de rota | Clientes sem rota hoje e com mais de uma compra, há mais de 90 dias sem comprar, ou que compraram nos últimos 30 dias com frequência histórica indefinida ou de pelo menos 30 dias | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |
