# regra_219.gobr

Regras de agendamento do time de televendas por tempo desde a última compra na empresa, em três faixas para quem já comprou com o próprio vendedor, mais uma regra para quem nunca comprou com ele. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal e os que compraram com qualquer vendedor da empresa nos últimos 25 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: compra recente na empresa | Clientes que compraram com qualquer vendedor da empresa nos últimos 25 dias | Não agendar |  |
| Nunca compraram com o vendedor | Clientes que nunca compraram com o próprio vendedor e nunca compraram na empresa ou estão há mais de 25 dias sem comprar nela | 21 dias |  |
| Compra entre 25 e 60 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias, mas estão há mais de 25 dias sem comprar, e já compraram com o próprio vendedor | 14 dias |  |
| Compra entre 60 e 90 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, e já compraram com o próprio vendedor | 7 dias |  |
| Inativos há mais de 90 dias | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa e já compraram com o próprio vendedor | 21 dias |  |
