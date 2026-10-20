# regra_063.gobr

Regras padrão de frequência para as carteiras fixas dos times de campo e de televendas. Em cada carteira, clientes ativos, inativos e sem vendas para o vendedor seguem a mesma frequência de 30 dias, com atendimento de segunda a sexta. Na televendas, os dias de atendimento devem evitar coincidir com os do time de campo. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa de todos os vendedores de televendas |
| carteira campo | Carteira fixa de todos os vendedores de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos (campo) | Clientes ativos para o vendedor, na carteira campo | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos (campo) | Clientes inativos para o vendedor, na carteira campo | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Sem vendas (campo) | Clientes que nunca compraram com o vendedor, na carteira campo | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Ativos (televendas) | Clientes ativos para o vendedor, na carteira televendas | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento; evitar coincidir com os dias do time campo |
| Inativos (televendas) | Clientes inativos para o vendedor, na carteira televendas | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento; evitar coincidir com os dias do time campo |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor, na carteira televendas | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento; evitar coincidir com os dias do time campo |
