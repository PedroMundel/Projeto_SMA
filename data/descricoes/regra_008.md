# regra_008.gobr

Regra de frequência de agendamento do time de campo, dividido em capital e interior, cada um com sua carteira fixa. Na carteira da capital, adimplentes e inadimplentes sem vendas são atendidos a cada 14 dias, e inadimplentes que já compraram a cada 30 dias. Na carteira do interior, todos os clientes são atendidos a cada 30 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira capital | Carteira fixa dos vendedores de campo do time capital |
| carteira interior | Carteira fixa dos vendedores do time interior (ids 35 e 34) |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Adimplentes (Capital) | Clientes adimplentes da carteira capital | 14 dias |  |
| Inadimplentes sem vendas (Capital) | Clientes inadimplentes da carteira capital que nunca compraram com o vendedor | 14 dias |  |
| Inadimplentes com vendas (Capital) | Clientes inadimplentes da carteira capital que já compraram com o vendedor, ativos ou inativos | 30 dias |  |
| Todos os clientes (Interior) | Todos os clientes da carteira interior | 30 dias |  |
