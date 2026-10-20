# regra_207.gobr

Regra de planejamento do time de televendas por tempo desde a última compra, em faixas até 14, 30, 45 e 90 dias, mais uma regra de resgate de inativos e uma para clientes sem vendas para o vendedor. Antes das faixas, deixam de ser agendados os clientes pessoa física. A regra de alta regularidade segue o histórico de visitas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Sem pedido | Clientes sem vendas para o vendedor | 14 dias |  |
| Ativos com alta regularidade | Clientes que compraram nos últimos 14 dias e têm alguma venda (ativos ou inativos) para o vendedor | Pelo histórico mais 7 dias, até 14 dias |  |
| Manter a regularidade | Clientes que compraram nos últimos 30 dias, mas estão há mais de 14 dias sem comprar, com alguma venda para o vendedor | 14 dias |  |
| Sem pedido entre 30 e 45 dias | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar, com alguma venda para o vendedor | 21 dias |  |
| Risco de ficar inativo | Clientes que compraram nos últimos 90 dias, mas estão há mais de 45 dias sem comprar, com alguma venda para o vendedor | 14 dias |  |
| Resgate de inativos | Clientes que estão há mais de 90 dias sem comprar e têm alguma venda para o vendedor | 28 dias |  |

## Pontos de atenção

- Clientes que nunca compraram e têm alguma venda (ativos ou inativos) para o vendedor não se enquadram em nenhuma regra e ficam sem parametrização.
