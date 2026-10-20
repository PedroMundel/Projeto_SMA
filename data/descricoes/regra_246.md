# regra_246.gobr

Regra de agendamento do time de televendas por ramo de atividade, em quatro carteiras, cada uma com uma faixa de clientes ativos e outra de inativos. Prospects são atendidos a cada 7 dias. O limite entre ativo e inativo é de 45, 60, 75 ou 90 dias sem comprar, conforme a carteira, com frequências entre 7 e 28 dias. Deixam de ser agendados os clientes baixados na Receita Federal e, na regra final, os que já compraram e não estão em nenhuma das carteiras.

## Carteiras

| Carteira | Descrição |
|---|---|
| ramos_1 | Carteira fixa dos vendedores de televendas com clientes de ramos como postos de combustível, farmácias, supermercados, redes, transporte e logística |
| ramos_2 | Carteira fixa dos vendedores de televendas com clientes de ramos como distribuidoras, materiais, gráficas, hospitais, laboratórios e indústrias |
| ramos_3 | Carteira fixa dos vendedores de televendas com clientes de ramos como alimentação, comércio, hotéis, oficinas, instituições e indústrias |
| ramos_4 | Carteira fixa dos vendedores de televendas com clientes de ramos como recarga de celular, vidraçaria, exportação, eventos, representantes e outros |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos da carteira ramos_1 | Clientes da carteira ramos_1 que compraram com qualquer vendedor da empresa nos últimos 45 dias | 14 dias |  |
| Inativos da carteira ramos_1 | Clientes da carteira ramos_1 que estão há mais de 45 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Ativos da carteira ramos_2 | Clientes da carteira ramos_2 que compraram com qualquer vendedor da empresa nos últimos 60 dias | 21 dias |  |
| Inativos da carteira ramos_2 | Clientes da carteira ramos_2 que estão há mais de 60 dias sem comprar com qualquer vendedor da empresa | 10 dias |  |
| Ativos da carteira ramos_3 | Clientes da carteira ramos_3 que compraram com qualquer vendedor da empresa nos últimos 75 dias | 28 dias |  |
| Inativos da carteira ramos_3 | Clientes da carteira ramos_3 que estão há mais de 75 dias sem comprar com qualquer vendedor da empresa | 14 dias |  |
| Ativos da carteira ramos_4 | Clientes da carteira ramos_4 que compraram com qualquer vendedor da empresa nos últimos 90 dias | 28 dias |  |
| Inativos da carteira ramos_4 | Clientes da carteira ramos_4 que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 14 dias |  |
| Demais clientes | Clientes que já compraram com qualquer vendedor da empresa e estão fora das carteiras ramos_1, ramos_2, ramos_3 e ramos_4 | Não agendar | Regra final: vale para quem sobrou das regras anteriores |
