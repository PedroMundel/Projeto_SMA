# regra_202.gobr

Regras de agendamento do time de televendas, organizadas por tempo desde a última compra e pelo relacionamento do cliente com o vendedor: sem compra há mais de 60 dias, clientes novos da carteira, novo relacionamento, alta frequência e estímulo de regularidade. Não há regras de bloqueio. Há clientes que não se enquadram em nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem compra em 60 dias | Clientes que estão há mais de 60 dias sem comprar | 7 dias |  |
| Ativar novo cliente | Clientes que nunca compraram ou compraram nos últimos 60 dias e não têm vendas para o vendedor | 7 dias |  |
| Novo relacionamento | Clientes que compraram nos últimos 60 dias, mas estão há mais de 7 dias sem comprar, com uma única compra com o vendedor | 7 dias |  |
| Alta frequência de compra | Clientes com vendas para o vendedor que compraram nos últimos 30 dias com mais de uma compra com ele, ou nos últimos 7 dias com uma única compra com ele | Pelo histórico, no máximo 30 dias |  |
| Estimular regularidade de compra | Clientes que compraram nos últimos 30 dias ou estão há mais de 60 dias sem comprar | 7 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Estimule a regularidade de compra do seu cliente' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- Clientes que nunca compraram ou compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com vendas para o vendedor e mais de uma compra com ele, ou que nunca compraram e têm uma única compra com o vendedor, não se enquadram em nenhuma regra e ficam sem parametrização.
