# regra_074.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes ativos para o vendedor são atendidos a cada 21 dias; inativos e clientes sem vendas, a cada 45 dias. Todas as faixas respeitam a preferência de dias configurada pelo vendedor.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | 45 dias | Respeita a preferência de dias configurada pelo vendedor |
| Ativos | Clientes ativos para o vendedor | 21 dias | Respeita a preferência de dias configurada pelo vendedor |
| Sem vendas | Clientes que nunca compraram com o vendedor | 45 dias | Respeita a preferência de dias configurada pelo vendedor |
