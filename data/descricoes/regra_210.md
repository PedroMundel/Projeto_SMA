# regra_210.gobr

Regra de agendamento do time de televendas com frequência única de 30 dias para quatro grupos: clientes com uma única compra, esquecidos, inativos sem compra e ativos fidelizados. Deixam de ser agendados as filiais, os inadimplentes e os clientes bloqueados para atendimento.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Ativado | Clientes com uma única compra com o vendedor | 30 dias |  |
| Esquecido | Clientes que compraram nos últimos 365 dias, mas estão há pelo menos 181 dias sem comprar, com mais de uma compra com o vendedor | 30 dias |  |
| Inativo | Clientes que estão há mais de 365 dias sem comprar, com mais de uma compra com o vendedor | 30 dias |  |
| Ativo fidelizado | Clientes que nunca compraram ou compraram nos últimos 180 dias, com mais de uma compra com o vendedor | 30 dias |  |
