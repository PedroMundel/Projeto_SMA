# regra_244.gobr

Regra de agendamento do time de televendas pelo ciclo de vida do cliente com o próprio vendedor, em seis faixas: prospect, ativado, ativo de compra regular, estímulo à regularidade, ruptura e inativo. Antes das faixas, deixam de ser agendados as filiais e os inadimplentes. Não há regra final para quem fica fora das faixas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospect | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativado | Clientes que já compraram com o próprio vendedor, mas têm uma única compra com ele | 7 dias |  |
| Ativo de compra regular | Clientes ativos para o vendedor, com mais de uma compra e frequência histórica de compra de até 7 dias | Pelo histórico, entre 5 e 7 dias |  |
| Estimular regularidade | Clientes com mais de uma compra que compraram com o próprio vendedor nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 14 dias | Entram os não ativos; ativos só se a frequência histórica for indefinida ou acima de 7 dias |
| Em ruptura | Clientes com mais de uma compra que compraram com o próprio vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Entram os não ativos; ativos só se a frequência histórica for indefinida ou acima de 7 dias |
| Inativos | Clientes com mais de uma compra que estão há mais de 60 dias sem comprar com o próprio vendedor | 14 dias | Entram os não ativos; ativos só se a frequência histórica for indefinida ou acima de 7 dias |

## Pontos de atenção

- Clientes que compraram com o próprio vendedor nos últimos 7 dias, não são de compra única e são não ativos (ou ativos com frequência histórica indefinida ou acima de 7 dias) não se enquadram em nenhuma regra e ficam sem parametrização.
