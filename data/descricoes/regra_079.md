# regra_079.gobr

Regra de agendamento do time de televendas por ramo de atividade. Clientes do ramo 12 são atendidos a cada 7 dias e os dos ramos 13, 14, 15, 16, 17, 18 e 19 a cada 14 dias. Clientes de qualquer outro ramo de atividade não são agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: outros ramos de atividade | Clientes com ramo de atividade diferente de 12, 13, 14, 15, 16, 17, 18 e 19 | Não agendar |  |
| Ramo de atividade 12 | Clientes com ramo de atividade 12 | 7 dias |  |
| Ramos de atividade 13 a 19 | Clientes com ramo de atividade 13, 14, 15, 16, 17, 18 ou 19 | 14 dias |  |
