# regra_055.gobr

Regra com três carteiras fixas: televendas, interior e capital. No televendas, adimplentes têm frequência de 14 dias, inadimplentes ativos e sem vendas de 30 dias, e inativos inadimplentes não são agendados. Na capital, clientes sem vendas e inadimplentes ficam em 30 dias e adimplentes em 14 dias. No interior, todos os clientes têm frequência de 30 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores de televendas |
| carteira interior | Carteira fixa dos vendedores do time interior |
| carteira capital | Carteira fixa dos vendedores de campo do time capital |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: adimplentes | Clientes adimplentes | 14 dias |  |
| Televendas: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias |  |
| Televendas: sem vendas inadimplentes | Clientes inadimplentes e sem vendas para o vendedor, exceto os já tratados pelas regras anteriores | 30 dias |  |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Capital: sem vendas | Clientes sem vendas para o vendedor | 30 dias |  |
| Capital: inadimplentes | Clientes inadimplentes e com alguma venda (ativos ou inativos) para o vendedor, exceto os já tratados pelas regras anteriores | 30 dias |  |
| Capital: adimplentes | Clientes adimplentes e com alguma venda (ativos ou inativos) para o vendedor, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Interior: todos os clientes | Todos os clientes | 30 dias |  |
