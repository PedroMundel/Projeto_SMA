# regra_243.gobr

Regra de agendamento do time de televendas para clientes pessoa jurídica, em três faixas de frequência: sem vendas para o vendedor, compra recente e compra entre 20 e 33 dias atrás. Não são agendados os clientes sem compra em 33 dias e os que não são pessoa jurídica. Todas as faixas atendem de segunda a sábado.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ative este cliente | Clientes pessoa jurídica sem vendas para o vendedor | 21 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Pós-vendas | Clientes pessoa jurídica com alguma venda para o vendedor que compraram nos últimos 20 dias | 3 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Cliente engajado | Clientes pessoa jurídica com alguma venda para o vendedor que compraram nos últimos 33 dias, mas estão há mais de 20 dias sem comprar | Pelo histórico mais 2 dias, entre 20 e 33 dias | Preferência de atendimento de segunda a sábado; demais dias sem atendimento |
| Bloqueio: sem compra em 33 dias | Clientes pessoa jurídica com alguma venda para o vendedor que nunca compraram ou estão há mais de 33 dias sem comprar | Não agendar |  |
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |

## Pontos de atenção

- O bloqueio 'Não agendar clientes sem compra em 33 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Ative este cliente!', 'Faça seu pós-vendas!' e 'Mantenha o cliente engajado!'.
