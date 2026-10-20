# regra_119.gobr

Regra de agendamento do time de televendas por situação do cliente no vendedor (ativo, inativo ou sem compra) e por adimplência. Ativos têm frequência de 15 dias se adimplentes e de 30 dias se inadimplentes; inativos adimplentes têm 7 dias; clientes sem compra têm 15 dias. Clientes inativos inadimplentes não são agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 15 dias |  |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 7 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem compra | Clientes sem vendas para o vendedor | 15 dias |  |
