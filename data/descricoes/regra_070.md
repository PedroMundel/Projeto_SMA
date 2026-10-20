# regra_070.gobr

Regra de agendamento para os times televendas (com carteira fixa) e campo, por situação do cliente: ativos, inativos e sem venda, com preferência de atendimento de segunda a sexta. Os ativos têm frequência de 14 dias e os inativos e sem venda do televendas, de 30 dias; no campo, os inativos seguem 30 dias. Não são agendados os inadimplentes inativos do televendas e os clientes sem venda do campo.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar | Carteira televendas |
| Ativos (televendas) | Clientes ativos para o vendedor | 14 dias | Carteira televendas; preferência de atendimento de segunda a sexta, demais dias sem atendimento |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 30 dias | Carteira televendas; preferência de atendimento de segunda a sexta, demais dias sem atendimento |
| Sem venda (televendas) | Clientes que nunca compraram com o vendedor | 30 dias | Carteira televendas; preferência de atendimento de segunda a sexta, demais dias sem atendimento |
| Ativos (campo) | Clientes ativos para o vendedor | 14 dias | Time campo; preferência de atendimento de segunda a sexta, demais dias sem atendimento |
| Inativos (campo) | Clientes inativos para o vendedor | 30 dias | Time campo; preferência de atendimento de segunda a sexta, demais dias sem atendimento |
| Bloqueio: sem venda (campo) | Clientes que nunca compraram com o vendedor | Não agendar | Time campo |
