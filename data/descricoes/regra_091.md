# regra_091.gobr

Regra padrão da empresa com configurações separadas para o time de televendas e para o time de campo, cada um com sua carteira fixa. No televendas, as faixas são por situação do cliente: ativos, inativos e sem vendas. No campo, ativos e inativos são ainda divididos entre adimplentes e inadimplentes, além dos clientes sem vendas. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |
| carteira campo | Carteira fixa dos vendedores do time campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: ativos | Clientes ativos para o vendedor | 14 dias |  |
| Televendas: inativos | Clientes inativos para o vendedor | 60 dias |  |
| Televendas: sem vendas | Clientes sem vendas para o vendedor | 14 dias |  |
| Campo: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Campo: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Campo: inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 30 dias |  |
| Campo: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 60 dias |  |
| Campo: sem vendas | Clientes sem vendas para o vendedor | 14 dias |  |
