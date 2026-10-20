# regra_233.gobr

Regra de agendamento do time de televendas por situação do cliente: ativos a cada 7 dias, inativos e clientes sem vendas a cada 14 dias. Antes dessas frequências, deixam de ser agendados os clientes com tipo de cobrança DH sem crédito, os com tipo de cobrança BK com crédito baixo e os inadimplentes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: BK com crédito baixo | Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |

## Pontos de atenção

- O nome da regra 'Não agendar clientes DH com crédito igual ou menor que R$0,00' cita R$ 0, valor que não aparece no código: nome e código podem estar divergentes.
- O nome da regra 'Não agendar clientes BK com crédito menor que R$200,00' cita R$ 200, valor que não aparece no código: nome e código podem estar divergentes.
