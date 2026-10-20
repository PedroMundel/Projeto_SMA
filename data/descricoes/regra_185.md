# regra_185.gobr

Regra de agendamento do time de televendas por ciclo de vida do cliente, em três faixas: prospects, ativos e inativos. Antes das faixas, deixam de ser agendados os clientes pessoa física e os baixados na Receita Federal.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Ativos | Clientes que já compraram na empresa e estão ativos no ciclo de vida | 7 dias |  |
| Inativos | Clientes que já compraram na empresa e estão fora do ciclo de vida ativo | 14 dias |  |
