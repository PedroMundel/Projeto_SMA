# regra_245.gobr

Regra de agendamento do time de televendas por carteiras de rota por cidade (todos os dias, segunda, terça, quarta, quinta e sexta). Em cada carteira, os clientes são separados entre com e sem visita na semana atual, e as rotas de dia específico têm dia de preferência de agendamento. Deixam de ser agendados os inadimplentes, os baixados na Receita Federal, os sem crédito e os que compraram nos últimos 60 dias. As duas últimas regras tratam as cidades não informadas nas rotas.

## Carteiras

| Carteira | Descrição |
|---|---|
| rota_todo_dia | Carteira fixa do time televendas com clientes das cidades da rota de todos os dias |
| rota_segunda | Carteira fixa do time televendas com clientes das cidades da rota de segunda |
| rota_terca | Carteira fixa do time televendas com clientes das cidades da rota de terça |
| rota_quarta | Carteira fixa do time televendas com clientes das cidades da rota de quarta |
| rota_quinta | Carteira fixa do time televendas com clientes das cidades da rota de quinta |
| rota_sexta | Carteira fixa do time televendas com clientes das cidades da rota de sexta |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: sem crédito | Clientes sem crédito disponível | Não agendar |  |
| Bloqueio: compra em 60 dias | Clientes que compraram nos últimos 60 dias | Não agendar |  |
| Rota todos os dias, com visita na semana | Clientes da carteira rota_todo_dia com visita na semana atual | Pelo histórico, entre 7 e 14 dias | Agenda para a semana seguinte; sem histórico, limitada a no mínimo 7 e no máximo 14 dias |
| Rota todos os dias, sem visita na semana | Clientes da carteira rota_todo_dia sem visita na semana atual | Pelo histórico mais 2 dias, entre 3 e 7 dias | Agenda para a semana corrente; sem histórico, limitada a no mínimo 3 e no máximo 7 dias |
| Rota terça, com visita na semana | Clientes da carteira rota_terca com visita na semana atual | 7 dias | Maior preferência de atendimento na segunda; demais dias sem atendimento |
| Rota terça, sem visita na semana | Clientes da carteira rota_terca sem visita na semana atual | 7 dias | Maior preferência de atendimento na segunda; demais dias sem atendimento |
| Rota quarta, com visita na semana | Clientes da carteira rota_quarta com visita na semana atual | 7 dias | Maior preferência de atendimento na terça; demais dias sem atendimento |
| Rota quarta, sem visita na semana | Clientes da carteira rota_quarta sem visita na semana atual | 7 dias | Maior preferência de atendimento na terça; demais dias sem atendimento |
| Rota quinta, com visita na semana | Clientes da carteira rota_quinta com visita na semana atual | 7 dias | Maior preferência de atendimento na quarta; demais dias sem atendimento |
| Rota quinta, sem visita na semana | Clientes da carteira rota_quinta sem visita na semana atual | 7 dias | Maior preferência de atendimento na quarta; demais dias sem atendimento |
| Rota sexta, com visita na semana | Clientes da carteira rota_sexta com visita na semana atual | 7 dias | Maior preferência de atendimento na quinta; demais dias sem atendimento |
| Rota sexta, sem visita na semana | Clientes da carteira rota_sexta sem visita na semana atual | 7 dias | Maior preferência de atendimento na quinta; demais dias sem atendimento |
| Rota segunda, com visita na semana | Clientes da carteira rota_segunda com visita na semana atual | 7 dias | Maior preferência de atendimento na sexta; demais dias sem atendimento |
| Rota segunda, sem visita na semana | Clientes da carteira rota_segunda sem visita na semana atual | 7 dias | Maior preferência de atendimento na sexta; demais dias sem atendimento |
| Cidades fora das rotas, com visita na semana | Clientes fora de todas as carteiras de rota (todo dia, segunda a sexta) com visita na semana atual | Pelo histórico, entre 7 e 14 dias | Agenda para a semana seguinte; sem histórico, limitada a no mínimo 7 e no máximo 14 dias |
| Cidades fora das rotas, sem visita na semana | Clientes fora de todas as carteiras de rota (todo dia, segunda a sexta) sem visita na semana atual | Pelo histórico menos 1 dia, entre 1 e 7 dias | Agenda para a semana corrente; sem histórico, limitada a no mínimo 1 e no máximo 7 dias |

## Pontos de atenção

- As carteiras 'rota_segunda' e 'rota_terca' compartilham 2 cidades (BRAGANCA PAULISTA, PIRACAIA): esses clientes aparecem nas duas.
- As carteiras 'rota_segunda' e 'rota_quarta' compartilham 15 cidades (AGUAS DE LINDOIA, AMPARO, ARACOIABA DA SERRA, BRAGANCA PAULISTA, CAMPO LIMPO PAULISTA e outras): esses clientes aparecem nas duas.
- As carteiras 'rota_segunda' e 'rota_quinta' compartilham 4 cidades (AGUAS DE SANTA BARBARA, BRAGANCA PAULISTA, ITATINGA, PIRACAIA): esses clientes aparecem nas duas.
- As carteiras 'rota_segunda' e 'rota_sexta' compartilham 3 cidades (ARACOIABA DA SERRA, CAMPO LIMPO PAULISTA, SAO PEDRO): esses clientes aparecem nas duas.
- As carteiras 'rota_terca' e 'rota_quarta' compartilham 4 cidades (BRAGANCA PAULISTA, PIRACAIA, SOROCABA, VOTORANTIM): esses clientes aparecem nas duas.
- As carteiras 'rota_terca' e 'rota_quinta' compartilham 25 cidades (ARTUR NOGUEIRA, BRAGANCA PAULISTA, CABREUVA, CAPIVARI, CONCHAL e outras): esses clientes aparecem nas duas.
- As carteiras 'rota_terca' e 'rota_sexta' compartilham 14 cidades (CORDEIROPOLIS, IRACEMAPOLIS, LIMEIRA, MAIRIPORA, NAZARE PAULISTA e outras): esses clientes aparecem nas duas.
- As carteiras 'rota_quarta' e 'rota_quinta' compartilham 2 cidades (BRAGANCA PAULISTA, PIRACAIA): esses clientes aparecem nas duas.
- As carteiras 'rota_quarta' e 'rota_sexta' compartilham 23 cidades (AGUAI, AGUAS DE SAO PEDRO, ARACOIABA DA SERRA, ARARAS, BOITUVA e outras): esses clientes aparecem nas duas.
