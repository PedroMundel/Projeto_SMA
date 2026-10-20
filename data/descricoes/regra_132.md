# regra_132.gobr

Regra de agendamento do time de televendas pelo histórico de compra com o próprio vendedor, em seis faixas: prospect, ativado, ativo regular, ativo a estimular, em ruptura e inativo. As frequências são de 7, 10 e 14 dias. Clientes inadimplentes não são agendados, e a última faixa, de inativos, fecha a regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospect - Cliente potencial | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Ativado - Fez um pedido e não comprou mais | Clientes que já compraram com o próprio vendedor, mas só uma única vez | 7 dias |  |
| Ativo - Compra regularmente | Clientes que já compraram com o próprio vendedor, com frequência histórica de compra de até 10 dias e sem ser de compra única | 14 dias |  |
| Ativo - Estimular a regularidade | Clientes que compraram nos últimos 59 dias, mas estão há mais de 10 dias sem comprar, com frequência histórica indefinida ou acima de 10 dias, e não de compra única | 10 dias | Considera as compras com o próprio vendedor |
| Em ruptura - Risco de ficar inativo | Clientes que compraram nos últimos 89 dias, mas estão há mais de 59 dias sem comprar, com frequência histórica indefinida ou acima de 10 dias, e não de compra única | 7 dias | Considera as compras com o próprio vendedor |
| Inativo - Reativar cliente sem compra | Clientes que compraram nos últimos 10 dias ou estão há mais de 89 dias sem comprar, com frequência histórica indefinida ou acima de 10 dias, e não de compra única | 10 dias | Considera as compras com o próprio vendedor |
