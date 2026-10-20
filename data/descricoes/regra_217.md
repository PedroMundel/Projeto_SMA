# regra_217.gobr

Regra de planejamento do time de televendas com duas faixas de frequência. Clientes com uma única compra com o vendedor são atendidos a cada 7 dias, e quem compra com regularidade segue a frequência calculada pelo histórico de visitas, entre 14 e 28 dias. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Relacionamento | Clientes com uma única compra com o vendedor | 7 dias |  |
| Manter a regularidade | Clientes com mais de uma compra com o vendedor que compraram nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar | Pelo histórico, entre 14 e 28 dias |  |

## Pontos de atenção

- Clientes com mais de uma compra com o vendedor que nunca compraram, compraram nos últimos 6 dias ou estão há mais de 30 dias sem comprar não se enquadram em nenhuma regra e ficam sem parametrização.
