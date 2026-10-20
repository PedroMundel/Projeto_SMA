# regra_178.gobr

Regra de agendamento dos times televendas_1 e televendas_2. O time televendas_1 organiza os clientes por tempo sem comprar em quatro faixas de reativação, todas com frequência de 7 ou 15 dias. Deixam de ser agendados os clientes baixados na Receita Federal, os cadastrados no ERP há pelo menos 7 dias (televendas_2) e os que compraram nos últimos 39 dias. As quatro regras por tempo de cadastro do televendas_2 nunca são aplicadas, e não há regra final para os demais clientes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: nunca compraram com a empresa | Clientes cadastrados no ERP há pelo menos 7 dias | Não agendar | Vale para o time televendas_2 |
| Bloqueio: compra recente | Clientes que compraram nos últimos 39 dias | Não agendar |  |
| Tentativa final | Clientes cadastrados no ERP há pelo menos 60 dias | 30 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Lead frio | Clientes cadastrados no ERP há pelo menos 30 dias | 20 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Lead morno | Clientes cadastrados no ERP há pelo menos 15 dias | 15 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Follow-up | Clientes cadastrados no ERP há mais de 7 dias | 15 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Estimular recompra | Clientes que compraram nos últimos 89 dias, mas estão há mais de 39 dias sem comprar | 15 dias |  |
| Reativação moderada | Clientes que compraram nos últimos 119 dias, mas estão há mais de 89 dias sem comprar | 7 dias |  |
| Reativação intensa | Clientes que compraram nos últimos 359 dias, mas estão há mais de 119 dias sem comprar | 7 dias |  |
| Resgate crítico | Clientes que estão há mais de 359 dias sem comprar | 7 dias |  |

## Pontos de atenção

- A regra 'Tentativa final' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Lead frio' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Lead morno' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Follow-up' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- Todos os clientes do time televendas_1 não se enquadram em nenhuma regra e ficam sem parametrização.
- Todos os clientes do time televendas_2 não se enquadram em nenhuma regra e ficam sem parametrização.
