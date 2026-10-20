# regra_102.gobr

Regra de frequência com dois grupos: a carteira fixa do time televendas, dividida em duas faixas, e o time campo, com faixa única. No televendas, inativos inadimplentes são atendidos a cada 30 dias e os demais clientes a cada 14 dias. Todos os clientes do campo são atendidos a cada 30 dias. Todas as faixas atendem de segunda a sexta e não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 30 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Televendas: ativos ou adimplentes | Clientes que não são inativos para o vendedor, ou que são inativos e adimplentes | 14 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Campo: todos os clientes | Clientes de qualquer perfil atendidos pelo time campo | 30 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
