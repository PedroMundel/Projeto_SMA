# regra_177.gobr

Regra de agendamento do time de televendas, aplicada à carteira fixa dos vendedores do time. Deixam de ser agendados os clientes com tipo de cobrança DH sem crédito, os com tipo BK e crédito baixo e os inadimplentes. Para os demais, a frequência é de 7 dias para ativos e de 14 dias para inativos e para quem nunca comprou com o vendedor.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: DH sem crédito | Clientes com tipo de cobrança DH e sem crédito disponível | Não agendar |  |
| Bloqueio: BK com crédito baixo | Clientes com tipo de cobrança BK e com menos de R$ 199 de crédito disponível | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 14 dias |  |
| Sem venda | Clientes que nunca compraram com o vendedor | 14 dias |  |

## Pontos de atenção

- O nome da regra 'DH com crédito igual ou menor que R$0,00' cita R$ 0, valor que não aparece no código: nome e regra podem estar divergentes.
- O nome da regra 'BK com crédito menor que R$200,00' cita R$ 200, valor que não aparece no código: nome e regra podem estar divergentes.
