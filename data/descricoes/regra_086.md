# regra_086.gobr

Regra de frequência aplicada à carteira fixa de todos os vendedores da empresa, organizada por adimplência e situação de compra do cliente. Ativos adimplentes têm 10 dias, ativos inadimplentes e inativos adimplentes têm 14 dias, e inativos inadimplentes têm 90 dias. A regra final cobre clientes sem vendas, com 21 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 10 dias |  |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 90 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 21 dias |  |
