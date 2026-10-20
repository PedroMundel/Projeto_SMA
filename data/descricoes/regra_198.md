# regra_198.gobr

Regra de agendamento do time de televendas por frequência, em cinco faixas: prospects, clientes com primeira compra, clientes que compraram recentemente com o próprio vendedor, ativos e inativos. Prospects são visitados a cada 25 dias, recém-ativados a cada 14 dias, ativos a cada 14 dias e inativos a cada 21 dias. Quem compra com frequência segue o ritmo do histórico de compras. Não há regras de bloqueio na agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 25 dias |  |
| Ativado: primeiro pedido | Clientes que estão há mais de 30 dias sem comprar com o próprio vendedor e têm uma única compra na empresa | 14 dias |  |
| Alta frequência de compra | Clientes que compraram com o próprio vendedor nos últimos 30 dias | Pelo histórico, entre 7 e 30 dias | Frequência calculada pelo histórico de compras; sem histórico, fica entre 7 dias e 30 dias |
| Ativos | Clientes ativos na empresa que já compraram e nunca compraram com o próprio vendedor ou estão há mais de 30 dias sem comprar com ele | 14 dias |  |
| Inativos | Clientes fora do ciclo de vida ativo da empresa que já compraram e nunca compraram com o próprio vendedor ou estão há mais de 30 dias sem comprar com ele | 21 dias |  |
