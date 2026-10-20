# regra_246.gobr

Regra de agendamento do time de televendas por ramo de atividade, com quatro carteiras de ramos e, em cada uma, uma faixa de ativos e uma de inativos (corte em 45, 60, 75 e 90 dias sem comprar), mais os prospects. Não são agendados os clientes baixados na Receita Federal. A regra final também não agenda quem já comprou e ficou fora de todas as carteiras.

## Carteiras

| Carteira | Descrição |
|---|---|
| ramos_1 | Carteira fixa dos vendedores do televendas, filtrada por ramos de atividade (ids 101009, 101016, 101025, 101101, 101102, 101103 e mais 6) |
| ramos_2 | Carteira fixa dos vendedores do televendas, filtrada por ramos de atividade (ids 101001, 101002, 101003, 101004, 101005, 101006 e mais 20) |
| ramos_3 | Carteira fixa dos vendedores do televendas, filtrada por ramos de atividade (ids 101008, 101010, 101017, 101018, 101019, 101020 e mais 28) |
| ramos_4 | Carteira fixa dos vendedores do televendas, filtrada por ramos de atividade (ids 101013, 101040, 102001, 102002, 201011, 201021 e mais 2) |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos - ramos_1 | Clientes da carteira ramos_1 que compraram com qualquer vendedor da empresa nos últimos 45 dias | 14 dias |  |
| Inativos - ramos_1 | Clientes da carteira ramos_1 que estão há mais de 45 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Ativos - ramos_2 | Clientes da carteira ramos_2 que compraram com qualquer vendedor da empresa nos últimos 60 dias | 21 dias |  |
| Inativos - ramos_2 | Clientes da carteira ramos_2 que estão há mais de 60 dias sem comprar com qualquer vendedor da empresa | 10 dias |  |
| Ativos - ramos_3 | Clientes da carteira ramos_3 que compraram com qualquer vendedor da empresa nos últimos 75 dias | 28 dias |  |
| Inativos - ramos_3 | Clientes da carteira ramos_3 que estão há mais de 75 dias sem comprar com qualquer vendedor da empresa | 14 dias |  |
| Ativos - ramos_4 | Clientes da carteira ramos_4 que compraram com qualquer vendedor da empresa nos últimos 90 dias | 28 dias |  |
| Inativos - ramos_4 | Clientes da carteira ramos_4 que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 14 dias |  |
| Demais clientes | Clientes que já compraram com qualquer vendedor da empresa e estão fora das carteiras ramos_1, ramos_2, ramos_3 e ramos_4 | Não agendar | Regra final: vale para quem sobrou das regras anteriores |
