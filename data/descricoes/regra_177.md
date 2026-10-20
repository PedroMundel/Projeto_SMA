# regra_177.gobr

Regra de agendamento da carteira fixa dos vendedores de televendas, por situação do cliente: ativos a cada 7 dias, inativos e sem vendas a cada 14 dias. Antes das frequências, deixam de ser agendados os clientes com tipo de cobrança DH sem crédito, os com tipo de cobrança BK e menos de R$ 199 de crédito e os inadimplentes.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: BK com pouco crédito | Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem venda | Clientes que nunca compraram com o vendedor | 14 dias |  |
