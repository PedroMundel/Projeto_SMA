# regra_187.gobr

Regra de agendamento do time de televendas para prospects e inativos, em cinco faixas de tempo sem comprar mais uma regra final de requalificação. Antes das faixas, deixam de ser agendados os clientes baixados na Receita, as filiais, os inadimplentes, os cadastrados no ERP há pelo menos 60 dias e os que compraram nos últimos 60 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: cadastro de 60 dias | Clientes cadastrados no ERP há pelo menos 60 dias | Não agendar |  |
| Bloqueio: compras em 60d | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Inativos recentes | Clientes sem comprar na empresa há mais de 60 dias que compraram no grupo de vendedores nos últimos 90 dias | 7 dias |  |
| Inativos médio | Clientes sem comprar na empresa há mais de 60 dias que compraram no grupo de vendedores nos últimos 120 dias, mas estão há mais de 90 dias sem comprar nele | 7 dias |  |
| Inativos antigos | Clientes sem comprar na empresa há mais de 60 dias que compraram no grupo de vendedores nos últimos 180 dias, mas estão há mais de 120 dias sem comprar nele | 14 dias |  |
| Requalificação de inativos | Clientes sem comprar na empresa há mais de 60 dias que compraram no grupo de vendedores nos últimos 360 dias, mas estão há mais de 180 dias sem comprar nele | 21 dias |  |
| Requalificar do zero | Clientes sem comprar na empresa há mais de 60 dias que nunca compraram no grupo de vendedores ou estão há mais de 360 dias sem comprar nele | 28 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A cascata mistura escopos de recência de compra (empresa toda no bloqueio 'Não agendar clientes com compras em 60d' e grupo de vendedores nas faixas de inativos), então as faixas podem se sobrepor ou deixar lacunas.
