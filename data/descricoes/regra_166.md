# regra_166.gobr

Regra de agendamento da carteira fixa do time de televendas, com frequência de 7 dias para clientes ativos e de 14 dias para inativos e para clientes sem vendas. Antes das faixas, deixam de ser agendados os clientes com tipo de cobrança DH sem crédito disponível, os com tipo de cobrança BK e menos de R$ 199 de crédito disponível e os inadimplentes.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa de todos os vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: BK com pouco crédito | Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Clientes ativos | Clientes ativos para o vendedor | 7 dias |  |
| Clientes inativos | Clientes inativos para o vendedor | 14 dias |  |
| Clientes sem venda | Clientes sem vendas para o vendedor | 14 dias |  |
