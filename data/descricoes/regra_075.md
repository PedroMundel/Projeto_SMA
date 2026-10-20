# regra_075.gobr

Regra de agendamento da carteira fixa dos vendedores de televendas, por situação do cliente. Antes das faixas, deixam de ser agendados os clientes inadimplentes. Os clientes adimplentes são organizados em três faixas: ativos a cada 7 dias, inativos e sem vendas a cada 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Sem venda adimplentes | Clientes adimplentes e sem vendas para o vendedor | 14 dias |  |
