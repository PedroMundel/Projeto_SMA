# regra_231.gobr

Regras de agendamento para três times: carteira_regional, carteira_reativacao e carteira_direta. A regional agenda a cada 7 dias quem comprou entre 30 e 150 dias atrás; a reativação agenda a cada 14 dias quem nunca comprou ou está há mais de 150 dias sem comprar; a direta agenda todos os clientes a cada 7 dias. Bloqueiam a agenda os clientes baixados na Receita, os que compraram nos últimos 30 dias (regional) e os que compraram nos últimos 150 dias (reativação).

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar | Vale para os três times |
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar | Time carteira_regional |
| Compra entre 30 e 150 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 150 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Time carteira_regional |
| Bloqueio: compra em 150 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 150 dias | Não agendar | Time carteira_reativacao |
| Clientes sem compra | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Time carteira_reativacao |
| Sem compra há mais de 150 dias | Clientes que estão há mais de 150 dias sem comprar com qualquer vendedor da empresa | 14 dias | Time carteira_reativacao |
| Todos os clientes | Clientes em geral, sem nenhum filtro | 7 dias | Time carteira_direta |

## Pontos de atenção

- Para os times carteira_regional, carteira_reativacao e carteira_direta, todos os clientes não se enquadram em nenhuma regra e ficam sem parametrização.
- Para o time carteira_regional, todos os clientes não se enquadram em nenhuma regra e ficam sem parametrização.
