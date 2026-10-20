# regra_153.gobr

Regra de planejamento da carteira fixa dos vendedores do time de televendas. Antes das frequências, deixam de ser agendados os clientes com tipo de cobrança DH sem crédito disponível, os com tipo de cobrança BK com menos de R$ 80 de crédito disponível e os inadimplentes. Os demais seguem 7 dias para ativos e 14 dias para inativos e clientes sem vendas.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: BK com pouco crédito | Clientes com tipo de cobrança BK e com menos de R$ 80 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes sem vendas para o vendedor | 14 dias |  |

## Pontos de atenção

- O nome da regra 'Não agendar clientes DH com crédito igual ou menor que R$0,00' fala em R$ 0, mas esse valor não aparece na regra.
- O nome da regra 'Não agendar clientes BK com crédito menor que R$200,00' fala em R$ 200, mas a regra usa outro valor.
