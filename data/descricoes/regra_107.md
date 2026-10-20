# regra_107.gobr

Regra de agendamento da carteira fixa de todos os vendedores da empresa, com frequência única de 15 dias para clientes inativos, ativos e sem vendas. Para ativos e inativos vale a preferência de dias configurada pelo vendedor. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa higicop | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | 15 dias | Preferência de dias configurada pelo vendedor |
| Ativos | Clientes ativos para o vendedor | 15 dias | Preferência de dias configurada pelo vendedor |
| Sem vendas | Clientes que nunca compraram com o vendedor | 15 dias |  |
