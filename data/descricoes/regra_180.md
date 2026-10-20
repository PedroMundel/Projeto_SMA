# regra_180.gobr

Regra de agendamento do time de televendas por ramo de atividade, em duas faixas: cinco ramos de atividade específicos com frequência curta e todos os demais ramos com frequência maior. Não são agendadas as filiais nem os clientes com situação suspensa, inapta ou baixada na Receita Federal. A última regra vale para os clientes de todos os ramos fora da lista.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: suspensos na Receita | Clientes com situação suspensa na Receita Federal | Não agendar |  |
| Bloqueio: inaptos na Receita | Clientes com situação inapta na Receita Federal | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Ramos 84, 73, 69, 85 e 22 | Clientes dos ramos de atividade 22, 69, 73, 84 e 85 | 7 dias |  |
| Demais ramos de atividade | Clientes de ramos de atividade fora de 22, 69, 73, 84 e 85 | 30 dias | Regra final: vale para quem sobrou da faixa anterior |
