# regra_047.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores habilitados. Os clientes são organizados por situação: ativos adimplentes, ativos inadimplentes, inativos adimplentes e sem vendas, com frequências de 7 e 14 dias. Deixam de ser agendados os clientes pessoa física e os inativos inadimplentes.

## Carteiras

| Carteira | Descrição |
|---|---|
| regra padrao | Carteira fixa de todos os vendedores habilitados no Govendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas | Clientes sem vendas para o vendedor | 14 dias |  |
