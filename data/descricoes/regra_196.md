# regra_196.gobr

Regra de agendamento do time de televendas por situação do cliente: prospects com frequência de 40 dias, ativos com 15 dias e inativos com 20 dias. Antes das faixas, deixam de ser agendados os inadimplentes e os clientes da cidade de Fortaleza que compraram nos últimos 60 dias. A faixa de inativos funciona como regra final para quem já comprou e não está ativo para o vendedor.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: Fortaleza com compra recente | Clientes da cidade de Fortaleza que compraram nos últimos 60 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 40 dias |  |
| Ativos adimplentes | Clientes que já compraram na empresa e estão ativos para o vendedor | 15 dias |  |
| Inativos adimplentes | Clientes que já compraram na empresa e não estão ativos para o vendedor | 20 dias | Regra final: vale para quem sobrou das faixas anteriores |
