# regra_082.gobr

Regra de frequência aplicada à carteira fixa de todos os vendedores da empresa, organizada por situação do cliente (ativo ou inativo para o vendedor) e por adimplência. Ativos adimplentes são atendidos a cada 7 dias, ativos inadimplentes a cada 14 dias e inativos adimplentes a cada 30 dias. Inativos inadimplentes não são agendados. Clientes sem vendas são atendidos a cada 30 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 30 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 30 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
