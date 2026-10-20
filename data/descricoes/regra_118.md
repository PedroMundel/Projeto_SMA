# regra_118.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes ativos para o vendedor seguem a frequência média dos ativos da empresa. Clientes inativos e os sem vendas seguem a frequência média dos inativos da empresa. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa dos vendedores do time empresa toda |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | Média dos inativos da empresa |  |
| Ativos | Clientes ativos para o vendedor | Média dos ativos da empresa |  |
| Sem vendas | Clientes sem vendas para o vendedor | Média dos inativos da empresa |  |
