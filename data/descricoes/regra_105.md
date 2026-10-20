# regra_105.gobr

Regra de agendamento da carteira fixa de todos os vendedores da empresa, organizada por situação do cliente (ativo, inativo ou sem vendas) e por adimplência. Ativos adimplentes têm frequência de 7 dias; os demais grupos agendados têm frequência de 14 dias, com atendimento de segunda a sexta. Inativos inadimplentes não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas | Clientes sem vendas para o vendedor | 14 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
