# regra_077.gobr

Regra de agendamento do time de televendas por situação do cliente: prospects, ativos e inativos. Antes das faixas, deixam de ser agendados os clientes bloqueados para atendimento, os inadimplentes e os que compraram nos últimos 30 dias. Prospects e inativos seguem frequência de 14 dias; ativos, 7 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: compra recente | Clientes que compraram nos últimos 30 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Clientes ativos | Clientes que já compraram na empresa e estão no ciclo de vida ativo | 7 dias |  |
| Clientes inativos | Clientes que já compraram na empresa e estão fora do ciclo de vida ativo | 14 dias |  |
