# regra_057.gobr

Regra de agendamento do time de televendas por situação de compra do cliente, em três grupos: prospects, ativos e inativos. Prospects e inativos são atendidos a cada 30 dias e os ativos, a cada 25 dias. Não há bloqueios de agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 30 dias |  |
| Ativos | Clientes que já compraram com algum vendedor da empresa e estão ativos para o vendedor | 25 dias |  |
| Inativos | Clientes que já compraram com algum vendedor da empresa, mas não estão ativos para o vendedor | 30 dias |  |
