# regra_064.gobr

Regras padrão de frequência para as carteiras fixas de televendas e de campo, separando clientes ativos, inativos e sem vendas, e por situação de adimplência. Em televendas, clientes inativos e inadimplentes não são agendados. A carteira de campo tem faixas equivalentes, sem bloqueio, e clientes sem vendas seguem 14 dias nas duas carteiras.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa de todos os vendedores de televendas |
| carteira campo | Carteira fixa de todos os vendedores de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor, na carteira televendas | 7 dias |  |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor, na carteira televendas | 14 dias |  |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor, na carteira televendas | 14 dias |  |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor, na carteira televendas | Não agendar |  |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor, na carteira televendas | 14 dias |  |
| Ativos adimplentes (campo) | Clientes adimplentes e ativos para o vendedor, na carteira campo | 7 dias |  |
| Ativos inadimplentes (campo) | Clientes inadimplentes e ativos para o vendedor, na carteira campo | 14 dias |  |
| Inativos adimplentes (campo) | Clientes adimplentes e inativos para o vendedor, na carteira campo | 14 dias |  |
| Inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor, na carteira campo | 30 dias |  |
| Sem vendas (campo) | Clientes que nunca compraram com o vendedor, na carteira campo | 14 dias |  |
