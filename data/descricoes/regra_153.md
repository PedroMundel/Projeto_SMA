# regra_153.gobr

Regra de agendamento da carteira fixa dos vendedores do time de televendas, por situação do cliente. Antes das frequências, deixam de ser agendados os clientes DH sem crédito, os clientes BK com pouco crédito e os inadimplentes. Depois, clientes ativos são atendidos a cada 7 dias, e inativos e sem vendas a cada 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: clientes DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: clientes BK com pouco crédito | Clientes com tipo de cobrança BK e com menos de R$ 80 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |
