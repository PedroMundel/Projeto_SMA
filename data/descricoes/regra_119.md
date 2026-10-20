# regra_119.gobr

Parametrização do time de televendas por situação de compra e de pagamento do cliente. Ativos adimplentes são atendidos a cada 15 dias, ativos inadimplentes a cada 30 dias, inativos adimplentes a cada 7 dias e clientes sem compra a cada 15 dias. Inativos inadimplentes não são agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 15 dias |  |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 7 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem compra | Clientes que nunca compraram com o vendedor | 15 dias |  |
