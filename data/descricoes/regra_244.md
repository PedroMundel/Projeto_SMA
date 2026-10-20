# regra_244.gobr

Regra de agendamento do time de televendas pelo histórico de compra do cliente com o próprio vendedor, em seis faixas: prospects, ativados, compra regular, estímulo, ruptura e inativos. Deixam de ser agendadas as filiais e os inadimplentes. As faixas usam frequências de 7 e 14 dias, ou o histórico de visitas entre 5 e 7 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativados | Clientes que já compraram com o próprio vendedor, em uma única compra | 7 dias |  |
| Ativos que compram regularmente | Clientes ativos para o vendedor, com mais de uma compra e frequência histórica de compra de até 7 dias | Pelo histórico, entre 5 e 7 dias |  |
| Estimular a regularidade | Clientes com mais de uma compra com o próprio vendedor, que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 14 dias | Vale para quem não entrou na faixa de frequência histórica |
| Em ruptura | Clientes com mais de uma compra com o próprio vendedor, que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Vale para quem não entrou na faixa de frequência histórica |
| Inativos | Clientes com mais de uma compra com o próprio vendedor, que estão há mais de 60 dias sem comprar | 14 dias | Vale para quem não entrou na faixa de frequência histórica |

## Pontos de atenção

- Clientes com mais de uma compra com o próprio vendedor que compraram nos últimos 7 dias, e que não são ativos ou têm frequência histórica indefinida ou de mais de 7 dias, não se enquadram em nenhuma regra e ficam sem parametrização.
