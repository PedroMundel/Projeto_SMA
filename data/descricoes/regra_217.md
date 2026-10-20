# regra_217.gobr

Regra de planejamento do time de televendas em duas faixas. Clientes com uma única compra com o vendedor são atendidos a cada 7 dias, e os que compraram nos últimos 30 dias e não são de compra única seguem uma frequência calculada pelo histórico de compras. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Relacionamento | Clientes com uma única compra com o vendedor | 7 dias |  |
| Regularidade de compra | Clientes que compraram nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar, e não são de compra única com o vendedor | Pelo histórico, entre 14 e 28 dias | Frequência calculada pelo histórico de compras; sem histórico, vale o mínimo de 14 e o máximo de 28 dias |

## Pontos de atenção

- Clientes que nunca compraram, compraram nos últimos 6 dias ou estão há mais de 30 dias sem comprar, e que não são de compra única, não se enquadram em nenhuma regra e ficam sem parametrização.
