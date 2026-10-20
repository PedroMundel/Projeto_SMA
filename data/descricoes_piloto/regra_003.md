# regra_003.gobr

Regra do time de televendas que primeiro deixa de agendar filiais, clientes visitados pelo externo na semana anterior, clientes com rota do externo nos próximos 7 dias e clientes que compraram nos últimos 7 dias. Depois define a frequência por tempo desde a última compra e por tempo de cadastro no ERP: prospects, prospects que fizeram um único pedido, faixas de 30, 60 e 90 dias e inativos. A regra de reativação e a regra genérica final nunca são aplicadas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: visita do externo na semana anterior | Clientes com última visita do representante externo na semana anterior | Não agendar |  |
| Bloqueio: rota do externo nos próximos 7 dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Bloqueio: compra nos últimos 7 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 7 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Prospects com um único pedido | Clientes que estão há mais de 7 dias sem comprar, cadastrados no ERP há pelo menos 60 dias e com uma única compra com o vendedor | 14 dias |  |
| Compra nos últimos 30 dias | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar, exceto os cadastrados no ERP há pelo menos 60 dias com compra única com o vendedor | 14 dias |  |
| Último pedido entre 31 e 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, exceto os cadastrados no ERP há pelo menos 60 dias com compra única com o vendedor | 7 dias |  |
| Último pedido entre 61 e 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto os cadastrados no ERP há pelo menos 60 dias com compra única com o vendedor | 3 dias |  |
| Compra nos últimos 14 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Inativos | Clientes que estão há mais de 90 dias sem comprar, exceto os cadastrados no ERP há pelo menos 60 dias com compra única com o vendedor | 14 dias |  |
| Demais clientes | Clientes de todo o time televendas, sem filtro | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Cliente estava inativo e foi reativado' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'REGRA GENÉRICA' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
