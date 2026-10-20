# regra_059.gobr

Regra de agendamento do time de televendas por ramo de atividade e situação do cliente (prospects, ativos e inativos), com frequências de 5, 7, 10, 15, 20 e 30 dias. Antes das faixas, deixam de ser agendados os clientes de ramos de atividade fora da lista permitida. A última regra reúne os inativos dos ramos 12, 14, 2, 5 e 7 e os casos do ramo 5 que sobraram das faixas anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: ramos de atividade específicos | Clientes de ramos de atividade (id) fora de: 10, 11, 12, 14, 15, 17 e mais 9 | Não agendar |  |
| Prospects dos ramos 2, 7, 11, 12, 14 e 19 | Clientes que nunca compraram na empresa e são dos ramos de atividade 11, 12, 14, 19, 2 e 7 | 30 dias |  |
| Ativos dos ramos 3, 4, 6, 8, 15 e 18 | Clientes ativos para o vendedor dos ramos de atividade 15, 18, 3, 4, 6 e 8 | 30 dias |  |
| Ativos dos ramos 7 e 17 | Clientes ativos para o vendedor que já compraram na empresa e são dos ramos 17 e 7, ou que nunca compraram e são do ramo 17 | 15 dias |  |
| Ativos dos ramos 10, 11, 14 e 19 | Clientes ativos para o vendedor que já compraram na empresa e são dos ramos 10, 11, 14 e 19, ou que nunca compraram e são do ramo 10 | 7 dias |  |
| Ativos dos ramos 2 e 12 | Clientes ativos para o vendedor que já compraram na empresa e são dos ramos de atividade 12 e 2 | 5 dias |  |
| Inativos dos ramos 3, 4, 6, 8, 15 e 18 | Clientes inativos para o vendedor dos ramos de atividade 15, 18, 3, 4, 6 e 8 | 30 dias |  |
| Inativos do ramo 17 | Clientes inativos para o vendedor do ramo de atividade 17 | 20 dias |  |
| Inativos do ramo 10 | Clientes inativos para o vendedor do ramo de atividade 10 | 15 dias |  |
| Inativos dos ramos 11 e 19 | Clientes inativos para o vendedor que já compraram na empresa e são dos ramos de atividade 11 e 19 | 10 dias |  |
| Inativos dos ramos 2, 7, 12 e 14 | Clientes inativos que já compraram dos ramos 12, 14, 2, 5 e 7; clientes ativos do ramo 5; e inativos do ramo 5 que nunca compraram | 5 dias | Regra final: vale para quem sobrou das faixas anteriores |
