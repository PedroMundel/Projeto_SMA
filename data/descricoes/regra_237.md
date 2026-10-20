# regra_237.gobr

Regra de agendamento do time de televendas por tempo sem comprar e frequência histórica de compra, sem carteiras nem bloqueios. Clientes sem vendas para o vendedor têm frequência fixa de 14 dias. Quem compra com regularidade segue o histórico, e as faixas de estímulo e resgate usam 14 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Clientes ativados | Clientes sem vendas para o vendedor | 14 dias |  |
| Compra com regularidade | Clientes com alguma venda para o vendedor que compraram nos últimos 30 dias, com frequência histórica de compra de menos de 30 dias | Pelo histórico, entre 0 e 30 dias |  |
| Estimular a regularidade | Clientes com alguma venda para o vendedor que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias | Compraram nos últimos 30 dias, há pelo menos 30 dias sem comprar, com histórico indefinido ou de pelo menos 30 dias |
| Clientes resgatados | Clientes com alguma venda para o vendedor, sem comprar há mais de 60 dias e com frequência histórica de compra de mais de 30 dias | 14 dias |  |
| Resgatar inativos | Clientes com alguma venda para o vendedor, sem comprar há mais de 60 dias e com frequência histórica indefinida ou de até 30 dias | 14 dias |  |

## Pontos de atenção

- Clientes que nunca compraram e têm alguma venda para o vendedor, ou que compraram nos últimos 29 dias com frequência histórica indefinida ou de pelo menos 30 dias, não se enquadram em nenhuma regra e ficam sem parametrização.
