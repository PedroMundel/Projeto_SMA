# regra_008.gobr

Regra padrão de frequência para dois times externos, cada um com sua carteira fixa: capital (todos os vendedores de campo, exceto os de id 35 e 34) e interior (vendedores de id 35 e 34). Na capital, adimplentes e inadimplentes sem vendas são agendados a cada 14 dias e inadimplentes com alguma venda a cada 30 dias; no interior, todos a cada 30 dias. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira capital | Carteira fixa dos vendedores do time capital |
| carteira interior | Carteira fixa dos vendedores do time interior |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Capital: adimplentes | Clientes adimplentes da carteira capital | 14 dias |  |
| Capital: inadimplentes sem venda | Clientes inadimplentes que nunca compraram com o vendedor, exceto os já tratados pela regra anterior | 14 dias |  |
| Capital: inadimplentes com venda | Clientes inadimplentes que já compraram com o vendedor, ativos ou inativos | 30 dias |  |
| Interior: todos os clientes | Todos os clientes da carteira interior | 30 dias |  |
