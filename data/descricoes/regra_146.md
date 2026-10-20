# regra_146.gobr

Regra de agendamento do time de televendas organizada por ramo de atividade, frequência histórica de compra e tempo desde a última compra. Os ramos de saúde e FOOD têm faixas próprias de 7 dias, seguidas de faixas para clientes potenciais, ativados, ativos, em ruptura e inativos. Deixam de ser agendados os clientes inadimplentes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Saúde | Clientes dos ramos de atividade 15, 37 e 43 | 7 dias |  |
| FOOD | Clientes dos ramos de atividade 25, 4 e 41 com frequência histórica de compra de 7 dias | 7 dias |  |
| Cliente potencial | Clientes sem vendas de ramos fora de 15, 25, 37, 4, 41, 43; ou dos ramos 25, 4, 41 com frequência histórica indefinida, menor ou maior que 7 dias | 30 dias | Nos ramos 25, 4, 41 com frequência histórica maior que 7 dias, só sem vendas para o vendedor |
| Ativado | Clientes com uma única compra com o vendedor nos últimos 30 dias, em ramos fora de 15, 25, 37, 4, 41, 43 ou em 25, 4, 41 | 30 dias | Nos ramos 25, 4, 41 vale com frequência histórica indefinida, menor ou maior que 7 dias |
| Ativo: compra regularmente | Clientes com frequência histórica de compra de menos de 21 dias, exceto os já tratados pelas regras anteriores | 21 dias |  |
| Em ruptura | Clientes que compraram com o próprio vendedor nos últimos 45 dias, mas estão há pelo menos 30 dias sem comprar, de ramos fora de 15, 37, 43 | 21 dias | Frequência histórica indefinida ou de pelo menos 21 dias; compra única exige mais de 30 dias sem comprar no grupo |
| Inativo | Clientes que estão há mais de 46 dias sem comprar com o próprio vendedor, de ramos fora de 15, 37, 43 | 45 dias | Frequência histórica indefinida ou de pelo menos 21 dias; compra única exige mais de 30 dias sem comprar no grupo |

## Pontos de atenção

- A condição da regra 'Ativo: compra regularmente' é fragmentada demais para resumir; ela vale para clientes com frequência histórica de compra de menos de 21 dias, exceto os já tratados pelas regras anteriores.
- A cascata mistura escopos de recência de compra (grupo na regra 'Ativado: Fez um pedido e ainda não comprou mais'; vendedor nas regras 'Em ruptura: risco de ficar inativo' e 'Inativo: reativar cliente sem compra'), então as faixas não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes de ramos fora de 15, 37, 43, com frequência histórica indefinida ou de pelo menos 21 dias, que compraram com o próprio vendedor nos últimos 29 dias (ou nos últimos 46 dias, mas há mais de 45 dias sem comprar) e já têm venda para o vendedor não se enquadram em nenhuma regra e ficam sem parametrização; quem tem compra única só entra nesse caso se está há mais de 30 dias sem comprar no grupo de vendedores.
