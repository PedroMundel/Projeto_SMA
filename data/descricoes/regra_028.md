# regra_028.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Os clientes são separados por situação para o vendedor: ativos seguem a frequência média dos ativos da empresa, e inativos e clientes sem vendas seguem a frequência média dos inativos da empresa. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa dos vendedores do time empresa toda, que reúne todos os vendedores |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | Média dos inativos da empresa |  |
| Ativos | Clientes ativos para o vendedor | Média dos ativos da empresa |  |
| Sem vendas | Clientes sem vendas para o vendedor | Média dos inativos da empresa |  |
