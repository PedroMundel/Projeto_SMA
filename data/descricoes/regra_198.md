# regra_198.gobr

Regra de agendamento do time de televendas por situação do cliente: prospects, clientes com primeiro pedido, clientes de alta frequência de compra, ativos e inativos. As frequências variam de 14 a 25 dias, e a dos clientes de alta frequência é calculada pelo histórico, entre 7 e 30 dias. Não há bloqueios nem regra final.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 25 dias |  |
| Ativado: boas-vindas ao primeiro pedido | Clientes com uma única compra na empresa, que estão há mais de 30 dias sem comprar com o próprio vendedor | 14 dias |  |
| Alta frequência de compra | Clientes que compraram com o próprio vendedor nos últimos 30 dias | Pelo histórico, entre 7 e 30 dias |  |
| Ativos | Clientes ativos na empresa que nunca compraram com o próprio vendedor ou estão há mais de 30 dias sem comprar com ele, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Inativos | Clientes inativos na empresa que nunca compraram com o próprio vendedor ou estão há mais de 30 dias sem comprar com ele, exceto os já tratados pelas regras anteriores | 21 dias |  |
