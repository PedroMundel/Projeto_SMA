# regra_046.gobr

Regra de frequência do televendas aplicada à carteira fixa de todos os vendedores. Os clientes são organizados por situação: ativos, inativos adimplentes, inativos inadimplentes e sem vendas. Não há bloqueios de agenda, e a última regra atende os clientes sem vendas.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira todos | Carteira fixa de todos os vendedores |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias |  |
| Sem vendas | Clientes sem vendas para o vendedor | 7 dias | Regra final: vale para quem sobrou das anteriores |
