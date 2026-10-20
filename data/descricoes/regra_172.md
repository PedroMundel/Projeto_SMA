# regra_172.gobr

Regra simples de frequência para o time de televendas, separando clientes ativos e não ativos para o vendedor. Os ativos são agendados a cada 7 dias e os não ativos a cada 14 dias. Antes disso, deixam de ser agendados os inadimplentes e as filiais.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes não ativos para o vendedor | 14 dias | Regra final: vale para quem sobrou dos ativos |
