# regra_062.gobr

Regra de frequência para duas carteiras fixas, a de televendas e a de campo, separando clientes por adimplência e por situação de atividade. Ativos adimplentes são atendidos a cada 7 dias, ativos inadimplentes e inativos adimplentes a cada 14 dias, e clientes sem vendas a cada 14 dias. Em televendas, inativos inadimplentes não são agendados; em campo, eles têm frequência de 30 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time de televendas |
| carteira campo | Carteira fixa dos vendedores do time de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor | 14 dias |  |
| Ativos adimplentes (campo) | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Ativos inadimplentes (campo) | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos adimplentes (campo) | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor | 30 dias |  |
| Sem vendas (campo) | Clientes que nunca compraram com o vendedor | 14 dias |  |
