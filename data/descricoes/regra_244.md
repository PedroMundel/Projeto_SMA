# regra_244.gobr

Regra de agendamento do time de televendas por situação de compra do cliente com o próprio vendedor, em seis faixas: prospect, compra única, ativo com frequência histórica de até 7 dias, regularidade, ruptura e inativo. Não são agendadas as filiais e os inadimplentes. Parte dos clientes com compra recente não cai em nenhuma faixa.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativados (compra única) | Clientes que já compraram com o próprio vendedor, mas apenas uma vez | 7 dias |  |
| Ativos de compra regular | Clientes ativos para o vendedor, com mais de uma compra e frequência histórica de compra de até 7 dias | Pelo histórico; sem histórico, entre 5 e 7 dias |  |
| Estimular regularidade | Clientes com mais de uma compra com o próprio vendedor, que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 14 dias | Não inclui ativos com frequência histórica de até 7 dias, tratados antes |
| Em ruptura | Clientes com mais de uma compra com o próprio vendedor, que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Não inclui ativos com frequência histórica de até 7 dias, tratados antes |
| Inativos | Clientes com mais de uma compra com o próprio vendedor, que estão há mais de 60 dias sem comprar | 14 dias | Não inclui ativos com frequência histórica de até 7 dias, tratados antes |

## Pontos de atenção

- Clientes que compraram com o próprio vendedor nos últimos 7 dias, sem ser de compra única, e que não são ativos ou têm frequência histórica indefinida ou de mais de 7 dias não se enquadram em nenhuma regra e ficam sem parametrização.
