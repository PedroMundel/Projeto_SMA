# regra_156.gobr

Regra de agendamento do time de todos os vendedores habilitados, por histórico de compra com o próprio vendedor. Prospects são atendidos a cada 14 dias, clientes com uma única compra a cada 10 dias, e os demais por ativos (7 dias) e inativos (14 dias). A agenda bloqueia apenas os clientes inadimplentes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Clientes com uma compra | Clientes que já compraram com o próprio vendedor, com uma única compra | 10 dias |  |
| Ativos | Clientes ativos para o vendedor, com mais de uma compra com ele | 7 dias |  |
| Inativos | Clientes que já compraram com o próprio vendedor, não são ativos e têm mais de uma compra com ele | 14 dias | Regra final: vale para quem sobrou das faixas anteriores |
