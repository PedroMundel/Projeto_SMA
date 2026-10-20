# regra_075.gobr

Regra padrão do time de televendas, aplicada à carteira fixa dos vendedores do time. Primeiro deixam de ser agendados os clientes inadimplentes; entre os adimplentes, os ativos são atendidos a cada 7 dias e os inativos e os sem vendas a cada 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa de todos os vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Sem vendas adimplentes | Clientes adimplentes que nunca compraram com o vendedor | 14 dias |  |
