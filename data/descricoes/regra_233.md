# regra_233.gobr

Regra de agendamento do time de televendas por situação do cliente: ativos são atendidos a cada 7 dias, inativos e clientes sem vendas a cada 14 dias. Antes das frequências, deixam de ser agendados os clientes com tipo de cobrança DH sem crédito disponível, os de tipo BK com menos de R$ 199 de crédito disponível e os inadimplentes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: BK com pouco crédito | Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Clientes ativos | Clientes ativos para o vendedor | 7 dias |  |
| Clientes inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |
