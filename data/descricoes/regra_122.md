# regra_122.gobr

Regra padrão do time de televendas aplicada à carteira fixa dos vendedores do time. Clientes inadimplentes não são agendados. Entre os adimplentes, ativos para o vendedor têm frequência de 14 dias, inativos de 30 dias e os sem vendas de 14 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos adimplentes | Clientes adimplentes e ativos para o vendedor | 14 dias |  |
| Inativos adimplentes | Clientes adimplentes e inativos para o vendedor | 30 dias |  |
| Sem vendas adimplentes | Clientes adimplentes e sem vendas para o vendedor | 14 dias |  |
