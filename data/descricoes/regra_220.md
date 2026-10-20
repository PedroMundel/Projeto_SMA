# regra_220.gobr

Regras de agendamento para três times: carteira regional, carteira reativacao e carteira direta. A regional agenda a cada 7 dias os clientes com mais de 30 dias sem comprar; a reativação agenda a cada 14 dias quem está há mais de 149 dias sem comprar ou não tem venda para o vendedor; a direta agenda todos a cada 7 dias. Bloqueiam a agenda a compra na empresa nos últimos 30 dias (regional) e, na reativação, os clientes com compra recente que já tiveram venda para o vendedor.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar | Time carteira regional |
| Regional: mais de 30 dias sem comprar | Clientes que nunca compraram ou estão há mais de 30 dias sem comprar com qualquer vendedor da empresa | 7 dias | Time carteira regional |
| Reativação: mais de 149 dias sem comprar | Clientes que estão há mais de 149 dias sem comprar com qualquer vendedor da empresa | 14 dias | Time carteira reativacao |
| Reativação: sem venda para o vendedor | Clientes que nunca compraram ou compraram na empresa nos últimos 149 dias, sem nenhuma venda para o vendedor | 14 dias | Time carteira reativacao |
| Bloqueio: compra recente com venda para o vendedor | Clientes que nunca compraram ou compraram na empresa nos últimos 149 dias, com alguma venda (ativos ou inativos) para o vendedor | Não agendar | Time carteira reativacao |
| Carteira direta | Clientes em geral, sem nenhum filtro | 7 dias | Time carteira direta |

## Pontos de atenção

- O nome da regra 'Regional: mais de 30 dias sem comprar' fala em 150 dias, mas a regra usa outro valor.
