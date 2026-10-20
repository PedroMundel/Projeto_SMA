# regra_066.gobr

Regras padrão de frequência para as carteiras fixas dos times de televendas (internos) e de campo (externos), por situação do cliente e adimplência, com atendimento de segunda a sexta. Ficam sem agenda, nas duas carteiras, os clientes inativos inadimplentes e os clientes sem vendas. Nas duas carteiras, clientes inativos adimplentes seguem 30 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira campo | Carteira fixa de todos os vendedores de campo |
| carteira televendas | Carteira fixa de todos os vendedores de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes (internos) | Clientes adimplentes e ativos para o vendedor, na carteira televendas | 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes (internos) | Clientes inadimplentes e ativos para o vendedor, na carteira televendas | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes (internos) | Clientes adimplentes e inativos para o vendedor, na carteira televendas | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (internos) | Clientes inadimplentes e inativos para o vendedor, na carteira televendas | Não agendar |  |
| Bloqueio: sem vendas (internos) | Clientes que nunca compraram com o vendedor, na carteira televendas | Não agendar |  |
| Ativos (externos) | Clientes ativos para o vendedor, na carteira campo | 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes (externos) | Clientes adimplentes e inativos para o vendedor, na carteira campo | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (externos) | Clientes inadimplentes e inativos para o vendedor, na carteira campo | Não agendar |  |
| Bloqueio: sem vendas (externos) | Clientes que nunca compraram com o vendedor, na carteira campo | Não agendar |  |
