# regra_133.gobr

Regra de agendamento para dois times, televendas e campo, cada um com sua carteira fixa. Os clientes inadimplentes não são agendados. No televendas, clientes ativos para o vendedor têm frequência de 7 dias e os demais de 14 dias. No campo, ativos têm 7 dias e os não ativos 15 dias, com parametrização fixa de frequência e dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |
| carteira campo | Carteira fixa dos vendedores do time campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos (televendas) | Clientes ativos para o vendedor | 7 dias |  |
| Inativos (televendas) | Clientes que não estão ativos para o vendedor | 14 dias |  |
| Ativos (campo) | Clientes ativos para o vendedor | 7 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |
| Inativos (campo) | Clientes que não estão ativos para o vendedor | 15 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |
