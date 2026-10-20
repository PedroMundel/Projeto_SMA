# regra_121.gobr

Agendamento do time de televendas conforme o ciclo de vida e o tempo desde a última compra. Não são agendados os clientes baixados na Receita Federal e as filiais. Clientes reativados e os com apenas uma compra têm frequência de 3 dias; os ativos seguem faixas de até 120 dias, e a regra final cobre quem sobrou das faixas anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Reativados | Clientes no ciclo de vida reativado com a empresa | 3 dias |  |
| Uma única compra | Clientes com uma única compra na empresa, fora do ciclo de vida reativado | 3 dias |  |
| Ativos recorrentes | Clientes que compraram nos últimos 30 dias, com mais de uma compra, fora do ciclo de vida reativado | Pelo histórico, entre 3 e 21 dias |  |
| Ativos (30 a 60 dias) | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com mais de uma compra, fora do ciclo reativado | 14 dias |  |
| Ativos (60 a 90 dias) | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra, fora do ciclo reativado | 21 dias |  |
| Ativos (90 a 120 dias) | Clientes que compraram nos últimos 120 dias, mas estão há mais de 90 dias sem comprar, com mais de uma compra, fora do ciclo reativado | 14 dias |  |
| Demais clientes | Clientes que nunca compraram ou estão há mais de 120 dias sem comprar, com mais de uma compra, fora do ciclo de vida reativado | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |
