# regra_078.gobr

Regra de frequência aplicada à carteira fixa dos vendedores da empresa toda. Os clientes são separados por situação (ativos ou inativos) e por adimplência: ativos adimplentes são atendidos a cada 7 dias, ativos inadimplentes e inativos adimplentes a cada 14 dias, e inativos inadimplentes a cada 30 dias. Clientes sem vendas para o vendedor também seguem 14 dias. Todas as faixas atendem de segunda a sexta e não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa comercial bh | Carteira fixa dos vendedores do time empresa toda |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Sem vendas | Clientes que nunca compraram com o vendedor | 14 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
