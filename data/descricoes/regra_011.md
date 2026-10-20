# regra_011.gobr

Regra de agendamento para os times de televendas e de campo, cada um com sua carteira fixa. Em televendas, clientes inativos e sem vendas são atendidos a cada 14 dias; em campo, clientes ativos, inativos adimplentes e sem vendas também a cada 14 dias, sempre com preferência de segunda a sexta. Não são agendados os clientes ativos de televendas e os inativos inadimplentes de campo.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |
| carteira campo | Carteira fixa dos vendedores do time de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: ativos (televendas) | Clientes ativos para o vendedor, na carteira televendas | Não agendar |  |
| Inativos (televendas) | Clientes inativos para o vendedor, na carteira televendas | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor, na carteira televendas | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor, na carteira campo | Não agendar |  |
| Ativos (campo) | Clientes ativos para o vendedor, na carteira campo | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Inativos adimplentes (campo) | Clientes adimplentes e inativos para o vendedor, na carteira campo | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
| Sem vendas (campo) | Clientes que nunca compraram com o vendedor, na carteira campo | 14 dias | Dias de preferência: segunda, terça, quarta, quinta, sexta; demais dias sem atendimento |
