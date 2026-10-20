# regra_174.gobr

Regra de agendamento do time de televendas pela relação do cliente com o próprio vendedor, em faixas de prospects, ativados, ativos, em ruptura e inativos. Antes das faixas, deixam de ser agendados os inadimplentes e os baixados na Receita Federal. As frequências são de 14, 21 ou 28 dias, ou calculadas pelo histórico de compras, e os ramos de atividade 18 e 9 recebem tratamento separado.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativados | Clientes que já compraram com o próprio vendedor, estão cadastrados no ERP há pelo menos 60 dias e têm uma única compra com ele | 21 dias |  |
| Ativos: alta frequência de compra | Clientes que compraram com o próprio vendedor nos últimos 30 dias e têm frequência histórica de compra de menos de 14 dias | Pelo histórico, entre 10 e 14 dias | Exclui quem tem compra única e cadastro no ERP há pelo menos 60 dias, já tratado antes |
| Ativos: compra regularmente (ramos 18 e 9) | Clientes dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, com frequência histórica de menos de 30 dias, exceto os já tratados antes | Pelo histórico, entre 14 e 21 dias |  |
| Ativos: compra regularmente (demais ramos) | Clientes que compraram com o próprio vendedor nos últimos 60 dias, fora dos ramos 18 e 9, com frequência histórica de menos de 30 dias, exceto os já tratados antes | 28 dias |  |
| Ativos: estimular regularidade (ramos 18 e 9) | Clientes dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar | 14 dias | Frequência histórica indefinida ou de pelo menos 30 dias; exclui compra única com cadastro no ERP há pelo menos 60 dias |
| Ativos: estimular regularidade (demais ramos) | Clientes fora dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar | 21 dias | Frequência histórica indefinida ou de pelo menos 30 dias; exclui compra única com cadastro no ERP há pelo menos 60 dias |
| Em ruptura (ramos 9 e 18) | Clientes dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Exclui quem tem compra única e cadastro no ERP há pelo menos 60 dias, já tratado antes |
| Em ruptura (demais ramos) | Clientes fora dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Exclui quem tem compra única e cadastro no ERP há pelo menos 60 dias, já tratado antes |
| Inativos | Clientes que estão há mais de 90 dias sem comprar com o próprio vendedor | 21 dias | Exclui quem tem compra única e cadastro no ERP há pelo menos 60 dias, já tratado antes |

## Pontos de atenção

- Clientes que compraram com o próprio vendedor nos últimos 20 dias e têm frequência histórica indefinida ou de pelo menos 30 dias (considerando compra única e tempo de cadastro no ERP) não se enquadram em nenhuma regra e ficam sem parametrização.
