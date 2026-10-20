# regra_138.gobr

Regra do time de todos os vendedores habilitados. Clientes inadimplentes não são agendados. Todos os demais clientes são atendidos a cada 7 dias, sem separar ativos, inativos e prospects.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Demais clientes | Todos os clientes | 7 dias | Regra final: vale para quem sobrou do bloqueio de inadimplentes |
