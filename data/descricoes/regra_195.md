# regra_195.gobr

Regra de agendamento do time de televendas com faixas por tempo desde a última compra e por histórico de compras na empresa, no grupo de vendedores e com o próprio vendedor. Antes das faixas, deixam de ser agendados pessoas físicas, baixados na Receita Federal e clientes que compraram nos últimos 7 dias. São seis faixas de frequência, de 7, 14 e 21 dias; a última atende quem sobrou das anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: pedido nos últimos 7 dias | Clientes que compraram nos últimos 7 dias | Não agendar |  |
| Comprou no mês | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 21 dias |  |
| Novos | Clientes que nunca compraram na empresa | 14 dias |  |
| Relacionamento | Clientes com uma única compra na empresa, que nunca compraram no grupo de vendedores ou estão há mais de 30 dias sem comprar nele | 21 dias |  |
| Regularidade de compra | Clientes com mais de uma compra, sem comprar no grupo há mais de 30 dias, que compraram com o próprio vendedor nos últimos 60 dias, mas não nos últimos 30 | 21 dias |  |
| Risco de inatividade | Clientes com mais de uma compra, sem comprar no grupo há mais de 30 dias, que compraram com o próprio vendedor nos últimos 90 dias, mas não nos últimos 60 | 7 dias |  |
| Resgate de inativos | Clientes com mais de uma compra, parados no grupo há mais de 30 dias, que nunca compraram com o próprio vendedor, compraram nos últimos 30 dias ou não compram com ele há mais de 90 | 14 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- As faixas misturam escopos de recência de compra (grupo de vendedores em 'Não agendar clientes com pedido em 7d' e 'Manter contato com cliente que comprou no mês'; próprio vendedor em 'Manter a regularidade de compra' e 'Atuar para que o cliente não fique inativo'), então podem se sobrepor ou deixar lacunas.
