# regra_156.gobr

Regra de agendamento do time de todos os vendedores, com frequência definida pelo histórico de compras do cliente com o próprio vendedor: prospects, clientes com uma única compra, ativos e inativos. Deixam de ser agendados os clientes inadimplentes, e a última faixa trata os inativos com mais de uma compra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Clientes com apenas 1 compra | Clientes que já compraram com o próprio vendedor e têm uma única compra com ele | 10 dias |  |
| Ativos | Clientes ativos para o vendedor, com mais de uma compra com ele | 7 dias |  |
| Inativos | Clientes que já compraram com o próprio vendedor, não estão ativos para ele e têm mais de uma compra com ele | 14 dias |  |
