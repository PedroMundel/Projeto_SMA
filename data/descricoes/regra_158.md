# regra_158.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, frequência histórica de compra e número de compras: prospects, cinco faixas de clientes com compra recente e os inativos há mais de 120 dias. Antes das faixas, deixam de ser agendados os clientes inadimplentes e os baixados na Receita Federal. Alguns clientes com compra recente ficam fora de todas as faixas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram com nenhum vendedor da empresa | 30 dias |  |
| Ativado: um pedido | Clientes que compraram nos últimos 45 dias, estão cadastrados no ERP há pelo menos 120 dias e têm uma única compra na empresa | 21 dias |  |
| Ativo: alta frequência de compra | Clientes que compraram nos últimos 45 dias com frequência histórica de compra de menos de 30 dias, exceto os de compra única cadastrados há pelo menos 120 dias | 14 dias |  |
| Ativo: compra regularmente | Clientes que compraram nos últimos 120 dias, mas estão há mais de 45 dias sem comprar, com frequência histórica de compra de menos de 120 dias | 30 dias | Também entram os que compraram nos últimos 45 dias com frequência histórica de compra entre 30 e 119 dias |
| Ativo: estimular regularidade | Clientes que compraram nos últimos 70 dias, mas estão há mais de 45 dias sem comprar, com frequência histórica indefinida ou de pelo menos 120 dias | 30 dias | Inclui também quem comprou nos últimos 45 dias e está há pelo menos 45 dias sem comprar |
| Em ruptura: risco de ficar inativo | Clientes que compraram nos últimos 120 dias, mas estão há mais de 70 dias sem comprar, com frequência histórica indefinida ou de pelo menos 120 dias | 21 dias |  |
| Inativo: reativar cliente sem compra | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 30 dias |  |

## Pontos de atenção

- Clientes que compraram nos últimos 44 dias, com frequência histórica indefinida ou de pelo menos 120 dias, e que não são de compra única (ou são de compra única e cadastrados no ERP há menos de 120 dias) não se enquadram em nenhuma regra e ficam sem parametrização.
