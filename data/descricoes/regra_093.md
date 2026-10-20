# regra_093.gobr

Regra padrão de frequência com três carteiras fixas, uma para cada time: televendas, campo capital e campo interior. Televendas e campo capital separam ativos adimplentes (7 dias), ativos inadimplentes (14 dias), inativos (30 dias) e clientes sem vendas (30 dias). O campo interior usa só ativos (14 dias), inativos (30 dias) e sem vendas (30 dias). Não há regras de bloqueio, e todas atendem de segunda a sexta.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira fixa time interior | Carteira fixa dos vendedores do time campo interior |
| carteira fixa time campo capital | Carteira fixa dos vendedores do time campo capital |
| carteira fixa time televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Televendas: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Televendas: inativos | Clientes inativos para o vendedor | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Televendas: sem vendas | Clientes que nunca compraram com o vendedor | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo capital: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo capital: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo capital: inativos | Clientes inativos para o vendedor | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo capital: sem vendas | Clientes que nunca compraram com o vendedor | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo interior: ativos | Clientes ativos para o vendedor | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo interior: inativos | Clientes inativos para o vendedor | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Campo interior: sem vendas | Clientes que nunca compraram com o vendedor | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
