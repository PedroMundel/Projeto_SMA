# regra_099.gobr

Regra de agendamento com dois times: televendas, por situação do cliente, e campo, com frequência única. No televendas, clientes sem venda e adimplentes com alguma venda são atendidos a cada 7 dias, e ativos inadimplentes a cada 30 dias. Inativos inadimplentes do televendas não são agendados. Todos os clientes do time campo são atendidos a cada 30 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: sem venda | Clientes que nunca compraram com o vendedor | 7 dias |  |
| Televendas: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Televendas: adimplentes | Clientes adimplentes com alguma venda, ativos ou inativos para o vendedor | 7 dias |  |
| Campo: todos os clientes | Clientes de qualquer perfil atendidos pelo time campo | 30 dias |  |
