# regra_202.gobr

Regra de agendamento do time de televendas por tempo desde a última compra e relação com o vendedor, em cinco regras: clientes sem compra há mais de 60 dias, novos clientes da carteira, relacionamento com cliente novo, alta frequência de compra e estímulo de regularidade. Não há regras de bloqueio. A regra final nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem compra há mais de 60 dias | Clientes que estão há mais de 60 dias sem comprar | 7 dias |  |
| Novo cliente na carteira | Clientes que nunca compraram ou compraram nos últimos 60 dias, sem vendas para o vendedor | 7 dias |  |
| Relacionamento com cliente novo | Clientes que compraram nos últimos 60 dias, mas estão há mais de 7 dias sem comprar, com uma única compra com o vendedor | 7 dias |  |
| Alta frequência de compra | Clientes que compraram nos últimos 30 dias e têm mais de uma compra com o vendedor; ou compraram nos últimos 7 dias e têm uma única compra | Pelo histórico, até 30 dias | Frequência calculada pelo histórico de compras; sem histórico, limitada a no máximo 30 dias |
| Estimular regularidade | Clientes que compraram nos últimos 30 dias ou estão há mais de 60 dias sem comprar | 7 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Estimule a regularidade de compra do seu cliente' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- Clientes que nunca compraram ou compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com vendas para o vendedor e mais de uma compra com ele, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes que nunca compraram, com vendas para o vendedor e uma única compra com ele, não se enquadram em nenhuma regra e ficam sem parametrização.
