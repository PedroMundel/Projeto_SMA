# regra_220.gobr

Regra padrão de frequência para três times: carteira regional, carteira reativação e carteira direta. A carteira regional não agenda quem comprou na empresa nos últimos 30 dias e atende os demais a cada 7 dias. A carteira reativação atende com 14 dias quem está há mais de 149 dias sem comprar e quem não tem vendas para o vendedor, e não agenda quem tem alguma venda para o vendedor e comprou recentemente na empresa. A carteira direta atende todos os clientes a cada 7 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra recente (Regional) | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar | Vale para o time carteira regional |
| Sem comprar há mais de 30 dias (Regional) | Clientes que nunca compraram na empresa ou estão há mais de 30 dias sem comprar | 7 dias | Vale para o time carteira regional |
| Mais de 149 dias sem comprar (Reativação) | Clientes que estão há mais de 149 dias sem comprar com qualquer vendedor da empresa | 14 dias | Vale para o time carteira reativação |
| Sem vendas para o vendedor (Reativação) | Clientes sem vendas para o vendedor que nunca compraram na empresa ou compraram nos últimos 149 dias | 14 dias | Vale para o time carteira reativação |
| Bloqueio: compra recente (Reativação) | Clientes com alguma venda para o vendedor que nunca compraram na empresa ou compraram nos últimos 149 dias | Não agendar | Vale para o time carteira reativação |
| Todos os clientes (Direta) | Todos os clientes do time carteira direta | 7 dias |  |

## Pontos de atenção

- O nome da regra 'Frequência de 7 dias (Carteira Regional)' fala em 150 dias, mas a regra usa outro valor.
