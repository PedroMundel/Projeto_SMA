# regra_051.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores habilitados da empresa. Os clientes são separados por atividade e pagamento: ativos adimplentes a cada 7 dias, e ativos inadimplentes, inativos adimplentes e sem venda a cada 14 dias. Inativos inadimplentes não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores habilitados da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
