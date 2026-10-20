# regra_053.gobr

Configuração padrão com duas carteiras fixas: uma dos vendedores de televendas e outra dos vendedores de campo. Em televendas, ativos adimplentes têm frequência de 14 dias, ativos inadimplentes de 30 dias, inativos adimplentes e clientes sem vendas de 7 dias. Os inativos inadimplentes de televendas não são agendados. Na carteira de campo, ativos, inativos e sem vendas seguem as frequências médias da empresa, respeitando a preferência de dias do vendedor.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa de todos os vendedores de televendas |
| regra padrao | Carteira fixa de todos os vendedores de campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor | 14 dias |  |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor | 30 dias |  |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 7 dias |  |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas (televendas) | Clientes sem vendas para o vendedor | 7 dias |  |
| Inativos (campo) | Clientes inativos para o vendedor | Média dos inativos da empresa | Respeita a preferência de dias configurada pelo vendedor |
| Ativos (campo) | Clientes ativos para o vendedor | Média dos ativos da empresa | Respeita a preferência de dias configurada pelo vendedor |
| Sem vendas (campo) | Clientes sem vendas para o vendedor | Média dos inativos da empresa | Respeita a preferência de dias configurada pelo vendedor |
