# regra_158.gobr

Regra de agendamento do time de televendas por situação do cliente: prospects, ativados, ativos (alta frequência, regular e estimular regularidade), em ruptura e inativos, combinando tempo desde a última compra e frequência histórica de compra. Antes das faixas, deixam de ser agendados os inadimplentes e os baixados na Receita Federal. A regra final trata quem está há mais de 120 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 30 dias |  |
| Ativados | Clientes que compraram nos últimos 45 dias, cadastrados no ERP há pelo menos 120 dias e com uma única compra na empresa | 21 dias |  |
| Ativos: alta frequência | Clientes que compraram nos últimos 45 dias e têm frequência histórica de compra de menos de 30 dias | 14 dias | Compra única só entra se cadastrado no ERP há menos de 120 dias |
| Ativos: compra regularmente | Clientes que compraram nos últimos 120 dias, mas estão há mais de 45 dias sem comprar, com frequência histórica de compra de menos de 120 dias | 30 dias | Inclui quem comprou nos últimos 45 dias com frequência histórica entre 30 e 119 dias |
| Ativos: estimular regularidade | Clientes que compraram nos últimos 70 dias, mas estão há mais de 45 dias sem comprar, com frequência histórica indefinida ou de pelo menos 120 dias | 30 dias | Inclui compra nos últimos 45 dias, mas há pelo menos 45 dias sem comprar, com a mesma frequência histórica |
| Em ruptura: risco de ficar inativo | Clientes que compraram nos últimos 120 dias, mas estão há mais de 70 dias sem comprar, com frequência histórica indefinida ou de pelo menos 120 dias | 21 dias |  |
| Inativos: reativar | Clientes que estão há mais de 120 dias sem comprar na empresa | 30 dias | Regra final de frequência |

## Pontos de atenção

- Clientes que compraram nos últimos 44 dias, com frequência histórica indefinida ou de pelo menos 120 dias, não se enquadram em nenhuma regra e ficam sem parametrização (compra única só se cadastrados no ERP há menos de 120 dias).
