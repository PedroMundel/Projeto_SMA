# regra_003.gobr

Regra de agendamento do time de televendas por tempo desde a última compra: prospects, prospect ativado, faixas de compra recente (até 30, 60 e 90 dias) e inativos há mais de 90 dias. Antes das faixas, deixam de ser agendadas as filiais e os clientes com visita do externo na semana anterior, com rota programada nos próximos 7 dias ou com compra nos últimos 7 dias. A regra de reativados e a regra genérica final nunca são aplicadas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: visita do externo na semana anterior | Clientes com última visita do representante externo na semana anterior | Não agendar |  |
| Bloqueio: rota do externo nos próximos 7 dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Bloqueio: compra nos últimos 7 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 7 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Prospect ativado | Clientes há mais de 7 dias sem comprar com a empresa, cadastrados no ERP há pelo menos 60 dias e com uma única compra com o vendedor | 14 dias |  |
| Compra nos últimos 30 dias | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar, exceto os já tratados pela regra de prospect ativado | 14 dias |  |
| Última compra entre 31 e 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados pela regra de prospect ativado | 7 dias |  |
| Última compra entre 61 e 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto os já tratados pela regra de prospect ativado | 3 dias |  |
| Reativados | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Inativos | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa, exceto os já tratados pela regra de prospect ativado | 14 dias |  |
| Demais clientes | Clientes do time televendas, sem filtro | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Cliente estava inativo e foi reativado' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Regra genérica' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
