# regra_114.gobr

Regras de agendamento organizadas por time: Jamile, ruptura Jamile, ruptura Elizangela, interior, capital e televendas, cada um com sua frequência. Os times de ruptura não agendam quem comprou com qualquer vendedor da empresa nos últimos 30 dias, e o de ruptura Elizangela também não agenda clientes bloqueados. Interior e capital não agendam inativos inadimplentes. Em capital e televendas, a última regra do time atende os clientes restantes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Time Jamile: todos os clientes | Clientes em geral, sem filtro adicional | 15 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento. |
| Bloqueio: compra recente (ruptura Jamile) | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar |  |
| Ruptura Jamile: demais clientes | Clientes em geral, sem filtro adicional | 14 dias |  |
| Bloqueio: compra recente (ruptura Elizangela) | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar |  |
| Bloqueio: clientes bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Ruptura Elizangela: demais clientes | Clientes em geral, sem filtro adicional | 14 dias |  |
| Bloqueio: inativos inadimplentes (interior) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Interior: ativos ou adimplentes | Clientes que não são inativos para o vendedor, ou que são inativos e adimplentes | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento. |
| Bloqueio: inativos inadimplentes (capital) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Capital: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento. |
| Capital: demais clientes | Clientes sem vendas para o vendedor, ou adimplentes com alguma venda (ativos ou inativos) para o vendedor | 14 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento. |
| Televendas: ativos | Clientes ativos para o vendedor | 15 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento. |
| Televendas: inativos e prospects | Clientes que não são ativos para o vendedor | 7 dias | Regra final do televendas. Dias de preferência: segunda a sexta; demais dias sem atendimento. |

## Pontos de atenção

- O nome da regra 'Frequencia de 14 dias para clientes a 30 dias sem comprar' (ruptura Jamile) fala em 30 dias, mas a regra usa outro valor.
- O nome da regra 'Frequencia de 14 dias para clientes a 30 dias sem comprar' (ruptura Elizangela) fala em 30 dias, mas a regra usa outro valor.
