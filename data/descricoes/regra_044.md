# regra_044.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes inativos para o vendedor seguem a frequência média dos inativos da empresa; ativos seguem a média dos ativos; clientes sem vendas seguem a média dos inativos. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | Média dos inativos da empresa |  |
| Ativos | Clientes ativos para o vendedor | Média dos ativos da empresa |  |
| Sem vendas | Clientes sem vendas para o vendedor | Média dos inativos da empresa |  |
