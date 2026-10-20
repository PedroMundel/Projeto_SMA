# regra_038.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores do time. Clientes ativos para o vendedor são atendidos a cada 7 dias; inativos adimplentes a cada 14 dias e inativos inadimplentes a cada 30 dias. Clientes sem vendas para o vendedor seguem 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira todos | Carteira fixa de todos os vendedores do time |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |
