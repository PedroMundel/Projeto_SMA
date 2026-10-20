# regra_167.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, com frequências de 7 a 60 dias. Primeiro vêm os clientes sem nenhuma compra e os de compra única; depois, os que têm mais de uma compra, separados em quatro faixas (até 30, 90, 120 e mais de 120 dias sem comprar). Só os clientes baixados na Receita Federal deixam de ser agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Primeira compra | Clientes que nunca compraram na empresa | 7 dias |  |
| Tirou o primeiro pedido | Clientes que já compraram na empresa e têm uma única compra | 15 dias |  |
| Ativo: compra em 30 dias | Clientes que compraram nos últimos 30 dias e têm mais de uma compra na empresa | Pelo histórico, entre 7 e 21 dias |  |
| Aumentar a regularidade de compra | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar, e têm mais de uma compra na empresa | 28 dias |  |
| Caminhando para inatividade | Clientes que compraram nos últimos 120 dias, mas estão há mais de 90 dias sem comprar, e têm mais de uma compra na empresa | 45 dias |  |
| Resgate de inativos | Clientes que estão há mais de 120 dias sem comprar na empresa e têm mais de uma compra | 60 dias |  |

## Pontos de atenção

- As faixas misturam medidas de tempo sem compra de escopos diferentes: 'Resgate de inativos' olha a empresa toda, enquanto 'Ativo: cliente que tem compra com a empresa em 30 dias', 'Aumentar a regularidade de compra' e 'Cliente caminhando para inatividade' olham o grupo de vendedores. Por isso as faixas podem se sobrepor ou deixar lacunas.
- Clientes que compraram na empresa nos últimos 120 dias, mas nunca compraram com o grupo de vendedores ou estão há mais de 120 dias sem comprar com ele, e têm mais de uma compra, não se enquadram em nenhuma regra e ficam sem parametrização.
