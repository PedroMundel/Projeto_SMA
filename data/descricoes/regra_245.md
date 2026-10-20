# regra_245.gobr

Regra de agendamento do time de televendas organizada em carteiras de rota por cidade: rota de todos os dias e rotas de segunda a sexta. Antes das rotas, deixam de ser agendados os inadimplentes, os baixados na Receita, os sem crédito e quem comprou nos últimos 60 dias. Cada rota tem duas regras, para clientes com e sem visita na semana atual; as rotas de dia fixo usam 7 dias, com um dia de preferência por rota. As cidades fora das rotas seguem a frequência pelo histórico, também separada por visita na semana.

## Carteiras

| Carteira | Descrição |
|---|---|
| rota_todo_dia | Carteira fixa do televendas com clientes das cidades da rota de todos os dias |
| rota_segunda | Carteira fixa do televendas com clientes das cidades da rota de segunda |
| rota_terca | Carteira fixa do televendas com clientes das cidades da rota de terça |
| rota_quarta | Carteira fixa do televendas com clientes das cidades da rota de quarta |
| rota_quinta | Carteira fixa do televendas com clientes das cidades da rota de quinta |
| rota_sexta | Carteira fixa do televendas com clientes das cidades da rota de sexta |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: sem crédito | Clientes sem crédito disponível | Não agendar |  |
| Bloqueio: compra em 60 dias | Clientes que compraram nos últimos 60 dias | Não agendar |  |
| Rota todos os dias, com visita na semana | Clientes da rota de todos os dias com visita na semana atual | Pelo histórico, entre 7 e 14 dias | Agendados para a semana seguinte |
| Rota todos os dias, sem visita na semana | Clientes da rota de todos os dias sem visita na semana atual | Pelo histórico mais 2 dias, entre 3 e 7 dias | Agendados para a semana corrente |
| Rota terça, com visita na semana | Clientes da rota de terça com visita na semana atual | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Rota terça, sem visita na semana | Clientes da rota de terça sem visita na semana atual | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Rota quarta, com visita na semana | Clientes da rota de quarta com visita na semana atual | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Rota quarta, sem visita na semana | Clientes da rota de quarta sem visita na semana atual | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Rota quinta, com visita na semana | Clientes da rota de quinta com visita na semana atual | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Rota quinta, sem visita na semana | Clientes da rota de quinta sem visita na semana atual | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Rota sexta, com visita na semana | Clientes da rota de sexta com visita na semana atual | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Rota sexta, sem visita na semana | Clientes da rota de sexta sem visita na semana atual | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Rota segunda, com visita na semana | Clientes da rota de segunda com visita na semana atual | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Rota segunda, sem visita na semana | Clientes da rota de segunda sem visita na semana atual | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Fora das rotas, com visita na semana | Clientes de cidades fora das rotas, com visita na semana atual | Pelo histórico, entre 7 e 14 dias | Agendados para a semana seguinte |
| Fora das rotas, sem visita na semana | Clientes de cidades fora das rotas, sem visita na semana atual | Pelo histórico menos 1 dia, entre 1 e 7 dias | Agendados para a semana corrente |

## Pontos de atenção

- As carteiras 'rota_segunda' e 'rota_terca' compartilham 2 cidades (BRAGANCA PAULISTA, PIRACAIA): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_segunda' e 'rota_quarta' compartilham 15 cidades (entre elas AGUAS DE LINDOIA, AMPARO, ARACOIABA DA SERRA, BRAGANCA PAULISTA, CAMPO LIMPO PAULISTA): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_segunda' e 'rota_quinta' compartilham 4 cidades (AGUAS DE SANTA BARBARA, BRAGANCA PAULISTA, ITATINGA, PIRACAIA): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_segunda' e 'rota_sexta' compartilham 3 cidades (ARACOIABA DA SERRA, CAMPO LIMPO PAULISTA, SAO PEDRO): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_terca' e 'rota_quarta' compartilham 4 cidades (BRAGANCA PAULISTA, PIRACAIA, SOROCABA, VOTORANTIM): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_terca' e 'rota_quinta' compartilham 25 cidades (entre elas ARTUR NOGUEIRA, BRAGANCA PAULISTA, CABREUVA, CAPIVARI, CONCHAL): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_terca' e 'rota_sexta' compartilham 14 cidades (entre elas CORDEIROPOLIS, IRACEMAPOLIS, LIMEIRA, MAIRIPORA, NAZARE PAULISTA): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_quarta' e 'rota_quinta' compartilham 2 cidades (BRAGANCA PAULISTA, PIRACAIA): os clientes dessas cidades aparecem nas duas.
- As carteiras 'rota_quarta' e 'rota_sexta' compartilham 23 cidades (entre elas AGUAI, AGUAS DE SAO PEDRO, ARACOIABA DA SERRA, ARARAS, BOITUVA): os clientes dessas cidades aparecem nas duas.
