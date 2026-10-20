# regra_203.gobr

Regra de agendamento do time de televendas por frequência histórica média de pedidos, em seis faixas, mais uma regra para quem comprou apenas uma vez. Antes das faixas, deixam de ser agendados os baixados na Receita Federal, as filiais, os inadimplentes, os clientes que nunca compraram com o vendedor e os que estão há mais de 95 dias sem comprar. A última faixa também recebe quem tem frequência histórica indefinida.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: filiais | Clientes com id do cliente principal diferente de 36979 e filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: prospects | Clientes que nunca compraram com o vendedor | Não agendar |  |
| Bloqueio: sem compra há mais de 95 dias | Clientes que estão há mais de 95 dias sem comprar | Não agendar |  |
| Compra única | Clientes com uma única compra na empresa | 28 dias |  |
| Frequência histórica de 0 a 7 dias | Clientes com frequência histórica de compra de até 7 dias, exceto os de compra única na empresa | 6 dias |  |
| Frequência histórica de 8 a 14 dias | Clientes com frequência histórica de compra entre 8 e 14 dias, exceto os de compra única na empresa | 9 dias |  |
| Frequência histórica de 15 a 21 dias | Clientes com frequência histórica de compra entre 15 e 21 dias, exceto os de compra única na empresa | 16 dias |  |
| Frequência histórica de 22 a 28 dias | Clientes com frequência histórica de compra entre 22 e 28 dias, exceto os de compra única na empresa | 23 dias |  |
| Frequência histórica de 29 a 38 dias | Clientes com frequência histórica de compra entre 29 e 38 dias, exceto os de compra única na empresa | 29 dias |  |
| Frequência histórica de 39 a 60 dias | Clientes com frequência histórica de compra entre 39 e 60 dias, exceto os de compra única na empresa | 35 dias |  |
| Frequência histórica acima de 60 dias ou indefinida | Clientes com frequência histórica indefinida ou de mais de 60 dias, exceto os de compra única na empresa | 55 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- O nome da regra 'entre 61 e 95 dias' fala em 95 dias, mas a regra usa outro valor.
