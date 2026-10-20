# regra_149.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em três faixas de ativos (até 7, 30, 60 e 90 dias), mais prospects e inativos. Antes das faixas, deixam de ser agendados os clientes que compraram nos últimos 7 dias. Todas as faixas têm frequência de 14 dias, com atendimento de segunda a sábado; a regra de inativos fecha a cadeia para quem passou de 90 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra nos últimos 7 dias | Clientes que compraram nos últimos 7 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Ativos entre 7 e 30 dias | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 14 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Ativos entre 30 e 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Ativos entre 60 e 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Inativos | Clientes sem compra no grupo de vendedores há mais de 90 dias ou que só compraram com vendedores de outros grupos | 14 dias | Regra final: vale para quem sobrou das faixas anteriores. Preferência de atendimento de segunda a sábado |
