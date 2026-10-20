# regra_207.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em cinco faixas, mais uma regra para clientes sem pedido com a empresa. Deixam de ser agendados os clientes pessoa física. Uma regra final de resgate atende os clientes que estão há mais de 90 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Sem pedido com a empresa | Clientes que nunca compraram com o vendedor | 14 dias |  |
| Ativos com alta regularidade | Clientes que compraram nos últimos 14 dias e têm alguma venda (ativos ou inativos) para o vendedor | Pelo histórico de compras mais 7 dias | Se não houver histórico, limitada a no máximo 14 dias |
| Manter a regularidade | Clientes que compraram nos últimos 30 dias, mas estão há mais de 14 dias sem comprar, e têm alguma venda (ativos ou inativos) para o vendedor | 14 dias |  |
| Sem pedido de 30 a 45 dias | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar, e têm alguma venda (ativos ou inativos) para o vendedor | 21 dias |  |
| Risco de ficar inativo | Clientes que compraram nos últimos 90 dias, mas estão há mais de 45 dias sem comprar, e têm alguma venda (ativos ou inativos) para o vendedor | 14 dias |  |
| Resgate de inativos | Clientes que estão há mais de 90 dias sem comprar e têm alguma venda (ativos ou inativos) para o vendedor | 28 dias | Regra final do time |

## Pontos de atenção

- Clientes que nunca compraram e têm alguma venda (ativos ou inativos) para o vendedor não se enquadram em nenhuma regra e ficam sem parametrização.
