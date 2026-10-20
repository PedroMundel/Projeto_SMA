# regra_167.gobr

Regra de agendamento do time de televendas pelo histórico de compras do cliente: primeira compra, quem tirou o primeiro pedido, clientes ativos e faixas de inatividade de 30, 90 e 120 dias, com frequências de 7 a 60 dias. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal. A última faixa resgata quem está há mais de 120 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Primeira compra | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Primeiro pedido | Clientes que já compraram com qualquer vendedor da empresa e têm uma única compra na empresa | 15 dias |  |
| Ativos | Clientes que compraram nos últimos 30 dias e não têm compra única na empresa | Pelo histórico de compras, entre 7 e 21 dias | Sem histórico de compras, a frequência fica limitada a no mínimo 7 e no máximo 21 dias |
| Regularidade de compra | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar, sem compra única na empresa | 28 dias |  |
| Caminhando para inatividade | Clientes que compraram nos últimos 120 dias, mas estão há mais de 90 dias sem comprar, sem compra única na empresa | 45 dias |  |
| Resgate de inativos | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e não têm compra única na empresa | 60 dias |  |

## Pontos de atenção

- As regras 'Ativo: cliente que tem compra com a empresa em 30 dias', 'Aumentar a regularidade de compra' e 'Cliente caminhando para inatividade' medem a recência de compra no grupo de vendedores, e 'Resgate de inativos' mede na empresa toda; faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes que compraram com a empresa nos últimos 120 dias, não têm compra única e nunca compraram no grupo de vendedores ou estão há mais de 120 dias sem comprar no grupo não se enquadram em nenhuma regra e ficam sem parametrização.
