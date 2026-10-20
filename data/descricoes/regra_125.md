# regra_125.gobr

Regra de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes ativos são atendidos a cada 7 dias, inativos adimplentes a cada 15 dias e clientes sem vendas a cada 20 dias. Clientes inativos inadimplentes não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 15 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Prospects | Clientes que nunca compraram com o vendedor | 20 dias |  |
