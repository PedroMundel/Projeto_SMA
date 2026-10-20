# regra_053.gobr

Configuração padrão com duas carteiras fixas: a do time de televendas e a dos vendedores de campo. No televendas, a frequência varia conforme o cliente seja ativo, inativo ou sem vendas e adimplente ou inadimplente, com 14, 30 e 7 dias. Inativos inadimplentes do televendas não são agendados. Na carteira dos vendedores de campo, ativos, inativos e sem vendas seguem a frequência média da empresa, respeitando a preferência de dias do vendedor.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores de televendas |
| regra padrao | Carteira fixa dos vendedores de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 14 dias |  |
| Televendas: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias |  |
| Televendas: inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 7 dias |  |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Televendas: sem vendas | Clientes sem vendas para o vendedor | 7 dias |  |
| Campo: inativos | Clientes inativos para o vendedor | Média dos inativos da empresa | Respeita a preferência de dias configurada pelo vendedor |
| Campo: ativos | Clientes ativos para o vendedor | Média dos ativos da empresa | Respeita a preferência de dias configurada pelo vendedor |
| Campo: sem vendas | Clientes sem vendas para o vendedor | Média dos inativos da empresa | Respeita a preferência de dias configurada pelo vendedor |
