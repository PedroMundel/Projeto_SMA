# regra_026.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes ativos para o vendedor seguem a frequência média dos ativos da empresa; inativos e clientes sem vendas seguem a frequência média dos inativos da empresa.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | Média dos inativos da empresa |  |
| Ativos | Clientes ativos para o vendedor | Média dos ativos da empresa |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | Média dos inativos da empresa |  |
