# regra_150.gobr

Regra de agendamento do time de televendas por tempo desde a última compra na empresa, com prospects, clientes caminhando para a inatividade e inativos. Antes das faixas, deixam de ser agendados os clientes que compraram nos últimos 45 dias. A última regra faz o resgate de quem está há mais de 89 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra nos últimos 45 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 45 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 28 dias |  |
| Caminhando para inatividade | Clientes que compraram com qualquer vendedor da empresa nos últimos 89 dias, mas estão há mais de 45 dias sem comprar | 14 dias |  |
| Inativos (resgate) | Clientes que estão há mais de 89 dias sem comprar com qualquer vendedor da empresa | 21 dias |  |
