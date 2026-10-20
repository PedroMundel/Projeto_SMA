# regra_193.gobr

Regra de agendamento do time de televendas, organizada em duas carteiras fixas por ramo de atividade: ramos específicos com frequência de 14 dias e os demais ramos com 21 dias, para clientes que compraram nos últimos 60 dias. Clientes fora dessas carteiras ou sem compra há mais de 60 dias têm frequência de 7 dias. Não são agendados filiais, baixados na Receita Federal e clientes com compra recente e rota futura do vendedor.

## Carteiras

| Carteira | Descrição |
|---|---|
| ramos_freq_14 | Carteira fixa dos vendedores de televendas, com clientes dos ramos de atividade 110, 120, 124, 2, 20, 21 e mais 26 |
| ramos_freq_21 | Carteira fixa dos vendedores de televendas, com clientes de ramos de atividade fora dessa lista, exceto os já alocados em ramos_freq_14 |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: fora da semana de cobertura | Clientes que compraram na empresa nos últimos 60 dias e têm data de rota futura do vendedor nos próximos 21 dias | Não agendar |  |
| Ramos específicos com venda em 60 dias | Clientes da carteira ramos_freq_14 que compraram na empresa nos últimos 60 dias | 14 dias |  |
| Demais ramos com venda em 60 dias | Clientes da carteira ramos_freq_21 que compraram na empresa nos últimos 60 dias | 21 dias |  |
| Todos os ramos sem venda em 60 dias | Clientes fora das carteiras ramos_freq_14 e ramos_freq_21, ou que nunca compraram ou estão há mais de 60 dias sem comprar na empresa | 7 dias | Regra final: vale para quem sobrou das regras anteriores |
