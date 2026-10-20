# regra_226.gobr

Regra de agendamento do time de televendas por relacionamento do cliente com a empresa: sem vendas, recém-ativados, compradores mensais, compradores com intervalo maior e clientes parados há mais de 120 dias. As frequências são de 7, 14 e 28 dias, ou o histórico de visitas com limite de 60 dias. Não há bloqueios; a última faixa, de mais de 180 dias, está sobreposta à anterior.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem vendas | Clientes sem vendas para a empresa | 7 dias |  |
| Cliente ativado | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias e têm uma única compra na empresa | 14 dias |  |
| Compradores mensais | Clientes com frequência histórica de compra de 30 dias, que compraram na empresa nos últimos 120 dias, mas estão há mais de 30 dias sem comprar, ou compraram nos últimos 30 dias sem ser de compra única | 28 dias |  |
| Compram mês sim, mês não | Clientes que compraram na empresa e com o próprio vendedor nos últimos 30 dias, mas estão há pelo menos 20 dias sem comprar, sem ser de compra única | Pelo histórico, no máximo 60 dias | Vale para frequência histórica indefinida, de menos de 30 dias, ou de mais de 30 dias com alguma venda para a empresa |
| Sem comprar há mais de 120 dias | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 14 dias |  |
| Sem comprar há mais de 180 dias | Clientes que estão há mais de 180 dias sem comprar com qualquer vendedor da empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Resgate seu cliente inativo! Ele está há mais de 180 dias sem comprar com a empresa' nunca é aplicada: todos os clientes dela já são tratados pela regra anterior 'Mantenha seu cliente ativo! Ele está há 120 dias sem comprar com a empresa'.
- A sequência mistura medidas diferentes de tempo sem comprar (na empresa e com o próprio vendedor); faixas assim podem se sobrepor ou deixar clientes sem regra.
- Clientes que compraram na empresa nos últimos 120 dias, mas estão há mais de 30 dias sem comprar, ou que compraram nos últimos 30 dias sem comprar com o próprio vendedor no período exigido, e que têm frequência histórica indefinida, de menos de 30 dias ou de mais de 30 dias com venda para a empresa, não se enquadram em nenhuma regra e ficam sem parametrização.
