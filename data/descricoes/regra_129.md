# regra_129.gobr

Regra de agendamento para todos os vendedores habilitados. Clientes ativos para o vendedor são atendidos a cada 7 dias e os não ativos, a cada 14 dias. Não são agendados os clientes inadimplentes nem as filiais, antes das regras de frequência.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Clientes ativos | Clientes ativos para o vendedor | 7 dias |  |
| Clientes inativos | Clientes que não estão ativos para o vendedor | 14 dias | Regra final: vale para quem sobrou da regra de ativos |
