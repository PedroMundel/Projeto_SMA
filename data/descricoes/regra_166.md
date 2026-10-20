# regra_166.gobr

Regra do time de televendas aplicada à carteira fixa de todos os vendedores do time. Deixam de ser agendados os clientes DH sem crédito, os clientes BK com pouco crédito e os inadimplentes. Os demais seguem frequência de 7 dias para ativos e de 14 dias para inativos e para clientes sem vendas.

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
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |

## Pontos de atenção

- O nome da regra 'DH sem crédito' fala em R$ 0, mas esse valor não aparece no código: nome e código podem estar divergentes.
- O nome da regra 'BK com pouco crédito' fala em R$ 200, mas esse valor não aparece no código, que usa outro limite: nome e código podem estar divergentes.
