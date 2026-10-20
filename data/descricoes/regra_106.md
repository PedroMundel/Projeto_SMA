# regra_106.gobr

Regra de agendamento com duas carteiras fixas, uma do time de televendas e outra do time de campo, cada uma com faixas por situação do cliente (ativo, inativo ou sem venda) e adimplência. Em televendas as frequências são de 10, 21, 14, 60 e 30 dias; em campo, de 30, 14 e 30 dias. Clientes inadimplentes do campo não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira campo | Carteira fixa dos vendedores de campo |
| carteira televendas | Carteira fixa dos vendedores de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 10 dias | Carteira de televendas |
| Televendas: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 21 dias | Carteira de televendas |
| Televendas: inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Carteira de televendas |
| Televendas: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | 60 dias | Carteira de televendas |
| Televendas: sem vendas | Clientes sem vendas para o vendedor | 30 dias | Carteira de televendas |
| Campo: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 30 dias | Carteira de campo |
| Campo: inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 14 dias | Carteira de campo |
| Bloqueio: inadimplentes (campo) | Clientes inadimplentes | Não agendar | Carteira de campo |
| Campo: sem vendas | Clientes adimplentes e sem vendas para o vendedor | 30 dias | Carteira de campo |
