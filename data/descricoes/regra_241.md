# regra_241.gobr

Regra de agendamento do time de televendas por ramo de atividade do cliente, em seis faixas de frequência de 7, 14 e 28 dias, separadas entre clientes de revenda e de consumo. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal. Clientes de ramos não mapeados também não são agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Revenda, 7 dias | Clientes com ramo de atividade (id) em: 106, 109, 139, 141, 142, 143 | 7 dias |  |
| Revenda, 14 dias | Clientes com ramo de atividade (id) em: 140, 146, 148 | 14 dias |  |
| Revenda, 28 dias | Clientes com ramo de atividade (id) igual a 138 | 28 dias |  |
| Consumo, 7 dias | Clientes com ramo de atividade (id) em: 108, 144, 147 | 7 dias |  |
| Consumo, 14 dias | Clientes com ramo de atividade (id) em: 100, 107, 110, 111, 112, 113 e mais 1 | 14 dias |  |
| Consumo, 28 dias | Clientes com ramo de atividade (id) igual a 114 | 28 dias |  |
| Bloqueio: ramos não mapeados | Clientes com ramo de atividade (id) fora de: 100, 106, 107, 108, 109, 110 e mais 15 | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |
