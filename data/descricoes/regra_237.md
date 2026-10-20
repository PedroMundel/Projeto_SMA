# regra_237.gobr

Regra de agendamento do time de televendas por situação de compra e frequência histórica do cliente, em cinco regras. Clientes sem vendas para o vendedor têm frequência de 14 dias; quem compra com regularidade segue a frequência calculada pelo histórico, limitada entre 0 e 30 dias. As demais regras de estímulo e resgate usam 14 dias. Não há regras de bloqueio, e há combinações de clientes sem nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Clientes ativados | Clientes sem vendas para o vendedor | 14 dias |  |
| Compra com regularidade | Clientes com alguma venda para o vendedor que compraram nos últimos 30 dias e têm frequência histórica de compra de menos de 30 dias | Pelo histórico, entre 0 e 30 dias | Frequência calculada pelo histórico de compras; se não houver, limitada a no mínimo 0 e no máximo 30 dias |
| Estimular a regularidade | Clientes com alguma venda para o vendedor que compraram nos últimos 60 dias e estão há mais de 30 dias sem comprar | 14 dias | Também: compra nos últimos 30 dias, parado há pelo menos 30 dias, histórico indefinido ou de pelo menos 30 dias |
| Clientes resgatados | Clientes com alguma venda para o vendedor que estão há mais de 60 dias sem comprar e têm frequência histórica de compra de mais de 30 dias | 14 dias |  |
| Resgatar inativos | Clientes com alguma venda para o vendedor que estão há mais de 60 dias sem comprar e têm frequência histórica indefinida ou de até 30 dias | 14 dias |  |

## Pontos de atenção

- Clientes que nunca compraram e têm alguma venda (ativos ou inativos) para o vendedor, ou que compraram nos últimos 29 dias com frequência histórica indefinida ou de pelo menos 30 dias e têm alguma venda para o vendedor, não se enquadram em nenhuma regra e ficam sem parametrização.
