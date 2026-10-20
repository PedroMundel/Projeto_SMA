# regra_022.gobr

Regra de agendamento para dois times: televendas e campo, este com carteira fixa própria. O time de televendas atende todos os clientes a cada 14 dias, de segunda a sexta. No campo, clientes sem vendas para o vendedor não são agendados; os demais são atendidos a cada 14 dias, de segunda a sexta.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira campo | Carteira fixa dos vendedores do time campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: todos os clientes | Clientes de todos os tipos atendidos pelo time de televendas | 14 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Bloqueio: sem venda (campo) | Clientes sem vendas para o vendedor | Não agendar | Vale para a carteira campo |
| Campo: ativos ou inativos | Clientes da carteira campo, exceto os já tratados pelas regras anteriores | 14 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
