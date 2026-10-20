# regra_181.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Os clientes são separados por adimplência e por serem ativos ou inativos para o vendedor, com frequências de 7, 14 e 30 dias, e os clientes sem vendas seguem 14 dias. Deixam de ser agendadas as filiais.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa cescom | Carteira fixa dos vendedores do time empresa toda, sem filtros |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Segue a preferência de dias configurada pelo vendedor |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Segue a preferência de dias configurada pelo vendedor |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Segue a preferência de dias configurada pelo vendedor |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias | Segue a preferência de dias configurada pelo vendedor |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |
