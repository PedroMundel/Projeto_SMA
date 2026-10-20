# regra_176.gobr

Regra de agendamento para a carteira fixa dos vendedores do time de televendas. Antes das frequências, deixam de ser agendados os clientes com tipo de cobrança DH sem crédito disponível, os com tipo de cobrança BK com menos de R$ 199 de crédito e os inadimplentes. Depois, clientes ativos para o vendedor têm frequência de 7 dias; inativos e sem vendas, 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: cobrança DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: cobrança BK com pouco crédito | Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes sem vendas para o vendedor | 14 dias |  |

## Pontos de atenção

- O nome da regra 'Não agendar clientes DH com crédito igual ou menor que R$0,00' fala em R$ 0, mas esse valor não aparece na regra: nome e regra podem estar divergentes.
- O nome da regra 'Não agendar clientes BK com crédito menor que R$200,00' fala em R$ 200, mas a regra usa R$ 199: nome e regra podem estar divergentes.
