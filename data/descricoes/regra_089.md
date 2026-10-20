# regra_089.gobr

Regra de agendamento do time de televendas por situação do cliente: prospects, ativos e inativos, estes últimos divididos entre adimplentes e inadimplentes. Adimplentes e prospects são atendidos a cada 7 dias e inadimplentes a cada 14 dias. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram na empresa | 7 dias |  |
| Ativos adimplentes | Clientes que já compraram na empresa, estão adimplentes e são ativos para o vendedor | 7 dias |  |
| Ativos inadimplentes | Clientes que já compraram na empresa, estão inadimplentes e são ativos para o vendedor | 14 dias |  |
| Inativos adimplentes | Clientes que já compraram na empresa, estão adimplentes e não são ativos para o vendedor | 7 dias |  |
| Inativos inadimplentes | Clientes que já compraram na empresa, estão inadimplentes e não são ativos para o vendedor | 14 dias |  |
