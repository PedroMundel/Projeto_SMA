# regra_076.gobr

Regra de agendamento do time de televendas por rota e tempo desde a última compra. Deixam de ser agendados os inadimplentes, os bloqueados para atendimento, os inativos para a empresa e quem comprou nos últimos 20 dias. Depois vêm as faixas: clientes com rota hoje, prospects, clientes ativados, clientes que compram regularmente e clientes em ruptura. A regra final 'Fora de rota' também bloqueia quem sobrou das faixas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: inativos | Clientes inativos para a empresa | Não agendar |  |
| Bloqueio: compra recente | Clientes que compraram na empresa nos últimos 20 dias | Não agendar |  |
| Rota hoje | Clientes que nunca compraram ou estão há mais de 20 dias sem comprar na empresa, com data de rota hoje | 1 dia |  |
| Prospects | Clientes que nunca compraram na empresa e não têm data de rota hoje | 7 dias |  |
| Cliente ativado | Clientes com uma única compra na empresa, há mais de 20 dias sem comprar e sem data de rota hoje | 15 dias |  |
| Compra regularmente | Clientes que compraram nos últimos 30 dias, mas há mais de 20 dias sem comprar, sem rota hoje, com frequência histórica menor que 30 dias e mais de uma compra | Pelo histórico, entre 5 e 30 dias |  |
| Em ruptura | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar, sem rota hoje e com mais de uma compra | 15 dias |  |
| Bloqueio: fora de rota | Clientes sem rota hoje, parados há mais de 90 dias ou há mais de 20 dias (compra nos últimos 30) com frequência histórica indefinida ou de pelo menos 30 dias | Não agendar | Regra final: vale para quem sobrou das faixas anteriores; só clientes com mais de uma compra na empresa |
