# regra_181.gobr

Regra padrão aplicada à carteira fixa de todos os vendedores da empresa. Filiais não são agendadas. Ativos adimplentes são atendidos a cada 7 dias; ativos inadimplentes e inativos adimplentes a cada 14 dias; inativos inadimplentes a cada 30 dias; clientes sem vendas a cada 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa cescom | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Respeita a preferência de dias configurada pelo vendedor |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Respeita a preferência de dias configurada pelo vendedor |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Respeita a preferência de dias configurada pelo vendedor |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias | Respeita a preferência de dias configurada pelo vendedor |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias |  |
