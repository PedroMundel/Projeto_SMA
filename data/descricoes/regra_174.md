# regra_174.gobr

Regra de agendamento do time de televendas por situação do cliente com o próprio vendedor: prospects, ativados, ativos, em ruptura e inativos. Antes das faixas, deixam de ser agendados os inadimplentes e os baixados na Receita Federal. As frequências são de 14, 21 e 28 dias ou calculadas pelo histórico de compras, e os ramos de atividade 18 e 9 têm faixas próprias. A última regra reativa os clientes há mais de 90 dias sem comprar com o próprio vendedor.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativados | Clientes que já compraram com o próprio vendedor, com uma única compra, cadastrados no ERP há pelo menos 60 dias | 21 dias |  |
| Ativos de alta frequência | Clientes que compraram com o próprio vendedor nos últimos 30 dias, com frequência histórica de compra de menos de 14 dias, exceto os de compra única cadastrados no ERP há pelo menos 60 dias | Pelo histórico, limitada entre 10 e 14 dias | Se não houver histórico, vale no mínimo 10 dias e no máximo 14 dias |
| Ativos que compram regularmente (ramos 18 e 9) | Clientes dos ramos de atividade 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, com frequência histórica de menos de 30 dias, exceto os já tratados pelas regras anteriores | Pelo histórico, limitada entre 14 e 21 dias | Se não houver histórico, vale no mínimo 14 dias e no máximo 21 dias |
| Ativos que compram regularmente (demais ramos) | Clientes de ramos de atividade fora de 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, com frequência histórica de menos de 30 dias, exceto os já tratados pelas regras anteriores | 28 dias |  |
| Estimular regularidade (ramos 18 e 9) | Clientes dos ramos de atividade 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar, com frequência histórica indefinida ou de pelo menos 30 dias | 14 dias | Exclui compra única com cadastro no ERP há pelo menos 60 dias |
| Estimular regularidade (demais ramos) | Clientes de ramos de atividade fora de 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar, com frequência histórica indefinida ou de pelo menos 30 dias | 21 dias | Exclui compra única com cadastro no ERP há pelo menos 60 dias |
| Em ruptura (ramos 9 e 18) | Clientes dos ramos de atividade 18 e 9 que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Exclui compra única com cadastro no ERP há pelo menos 60 dias |
| Em ruptura (demais ramos) | Clientes de ramos de atividade fora de 18 e 9 que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Exclui compra única com cadastro no ERP há pelo menos 60 dias |
| Inativos | Clientes que estão há mais de 90 dias sem comprar com o próprio vendedor | 21 dias | Exclui compra única com cadastro no ERP há pelo menos 60 dias |

## Pontos de atenção

- A condição da regra R6 (Ativo: compra regularmente, frequência do histórico) é fragmentada demais para resumir; foi descrita pela condição própria, exceto os clientes já tratados pelas regras anteriores.
- A condição da regra R7 (Ativo: compra regularmente, 28 dias) é fragmentada demais para resumir; foi descrita pela condição própria, exceto os clientes já tratados pelas regras anteriores.
- Clientes que compraram com o próprio vendedor nos últimos 20 dias, com frequência histórica indefinida ou de pelo menos 30 dias, exceto os de compra única cadastrados no ERP há pelo menos 60 dias, não se enquadram em nenhuma regra e ficam sem parametrização.
