# regra_183.gobr

Regra de agendamento do time de televendas, que deixa de agendar os clientes inadimplentes. Prospects são atendidos a cada 21 dias; quem já comprou segue a frequência do histórico, entre 5 e 30 dias, ou 14 dias, conforme a frequência histórica de compra, e os inativos a cada 21 dias. Há clientes que não se enquadram em nenhuma regra e uma regra que nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 21 dias |  |
| Alta frequência de compra | Clientes que já compraram na empresa, ativos para o vendedor e com frequência histórica de compra de menos de 30 dias | Pelo histórico, entre 5 e 30 dias |  |
| Compra regularmente (sem pedido em 30 dias) | Clientes que já compraram na empresa, ativos para o vendedor e com frequência histórica de compra de mais de 30 dias | 14 dias |  |
| Compra regularmente (com pedido em 30 dias) | Clientes que compraram com o próprio vendedor nos últimos 30 dias, com frequência histórica de compra de mais de 30 dias e ativos para o vendedor | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Inativos | Clientes inativos no ciclo de vida da empresa que não estão ativos para o vendedor, ou que estão ativos mas têm frequência histórica indefinida ou de 30 dias | 21 dias |  |

## Pontos de atenção

- A regra 'Com pedido em 30d' (Compra regularmente) nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- Clientes que já compraram na empresa e não estão inativos no ciclo de vida da empresa, e que não são ativos para o vendedor ou são ativos com frequência histórica indefinida ou de 30 dias, não se enquadram em nenhuma regra e ficam sem parametrização.
