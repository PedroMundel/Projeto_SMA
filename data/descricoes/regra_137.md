# regra_137.gobr

Regras de agendamento para todos os vendedores da empresa, organizadas em três grupos de clientes. Prospects e inativos para o vendedor são atendidos a cada 14 dias, e os ativos para o vendedor, a cada 21 dias. Não há bloqueios de agenda, e a última regra cobre os demais clientes que já compraram na empresa.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Ativos | Clientes que já compraram na empresa e são ativos para o vendedor | 21 dias |  |
| Inativos | Clientes que já compraram na empresa e não são ativos para o vendedor | 14 dias | Regra final: vale para quem sobrou das anteriores |
