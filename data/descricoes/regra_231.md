# regra_231.gobr

Regra de agendamento para três times de carteira: regional, reativação e direta. Clientes baixados na Receita Federal não são agendados em nenhum dos times; no time regional também não são agendados os que compraram nos últimos 30 dias, e no de reativação os que compraram nos últimos 150 dias. O time regional atende a cada 7 dias quem comprou entre 30 e 150 dias atrás, o de reativação atende a cada 14 dias quem nunca comprou ou está há mais de 150 dias sem comprar, e o time direto atende todos os clientes a cada 7 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar | Vale para os times carteira_regional, carteira_reativacao e carteira_direta |
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar | Time carteira_regional |
| Compra entre 30 e 150 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 150 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Time carteira_regional |
| Bloqueio: compra nos últimos 150 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 150 dias | Não agendar | Time carteira_reativacao |
| Clientes sem compra | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Time carteira_reativacao |
| Sem compra em 150 dias | Clientes que estão há mais de 150 dias sem comprar com qualquer vendedor da empresa | 14 dias | Time carteira_reativacao |
| Todos os clientes | Todos os clientes | 7 dias | Time carteira_direta |

## Pontos de atenção

- Todos os clientes dos times carteira_regional, carteira_reativacao e carteira_direta aparecem como não enquadrados em nenhuma regra e ficam sem parametrização.
- Todos os clientes do time carteira_regional também aparecem como não enquadrados em nenhuma regra e ficam sem parametrização.
