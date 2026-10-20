# regra_007.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores de televendas. Clientes ativos para o vendedor são agendados a cada 14 dias, inativos a cada 30 dias e clientes sem vendas a cada 7 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos | Clientes inativos para o vendedor | 30 dias |  |
| Ativos | Clientes ativos para o vendedor | 14 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 7 dias |  |
