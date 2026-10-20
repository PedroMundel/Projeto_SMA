# regra_113.gobr

Regra de frequência aplicada à carteira fixa de todos os vendedores da empresa, organizada pela situação do cliente (sem vendas, ativo ou inativo) e por adimplência. Clientes sem vendas e ativos adimplentes são atendidos a cada 30 dias; ativos inadimplentes e inativos adimplentes, a cada 60 dias. Todas as faixas têm preferência de atendimento de segunda a sexta. Inativos inadimplentes não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem vendas | Clientes que nunca compraram com o vendedor | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 60 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 60 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
