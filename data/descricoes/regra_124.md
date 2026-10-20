# regra_124.gobr

Regra de frequência para os times de campo e de televendas. O time de campo atende todos os clientes a cada 30 dias. O televendas atende a cada 25 dias ativos, inativos adimplentes, inativos inadimplentes e clientes sem vendas, de segunda a sexta e evitando coincidir os dias com o time de campo.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Todos os clientes (campo) | Todos os clientes do time de campo | 30 dias |  |
| Ativos (televendas) | Clientes ativos para o vendedor | 25 dias | Preferência de segunda a sexta; evita coincidir os dias de atendimento com os do time campo |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 25 dias | Preferência de segunda a sexta; evita coincidir os dias de atendimento com os do time campo |
| Inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | 25 dias | Preferência de segunda a sexta; evita coincidir os dias de atendimento com os do time campo |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor | 25 dias | Preferência de segunda a sexta; evita coincidir os dias de atendimento com os do time campo |
