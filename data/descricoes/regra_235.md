# regra_235.gobr

Regra de agendamento de quatro times de televendas (felipe, paola_1, paola_2 e temporario_2meses), organizada por tempo desde a última compra e por data de rota. Não são agendados os baixados na Receita Federal, os clientes com rota futura ou compra nos últimos 7 dias (paola_1 e paola_2) e os com compra nos últimos 30 dias (felipe). O time felipe tem duas faixas de frequência, o paola_1 e paola_2 têm seis, e o temporario_2meses tem uma. Quem não se enquadra em nenhuma faixa também não é agendado.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar | Vale para os times felipe, paola_1, paola_2 e temporario_2meses |
| Bloqueio: rota futura em 7 dias | Clientes com data de rota futura nos últimos 7 dias | Não agendar | Times paola_1 e paola_2 |
| Bloqueio: compra em 7 dias | Clientes que compraram nos últimos 7 dias | Não agendar | Times paola_1 e paola_2 |
| Bloqueio: compra em 30 dias | Clientes que compraram nos últimos 30 dias | Não agendar | Time felipe |
| Cobertura de rota (14 dias depois) | Clientes com data de rota há 14 dias e com pelo menos 5% do limite de crédito disponível | 1 dia | Time temporario_2meses; preferência segunda a sábado |
| Compra entre 30 e 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar | 15 dias | Time felipe; preferência segunda a sábado |
| Sem compra em 90 dias | Clientes que nunca compraram ou estão há mais de 90 dias sem comprar | 10 dias | Time felipe; preferência segunda a sábado |
| Rota há 7 dias ou mais | Clientes que nunca compraram ou estão há mais de 7 dias sem comprar, com rota nos últimos 7 dias e pelo menos 5% do limite de crédito disponível | 14 dias | Times paola_1 e paola_2; preferência segunda a sábado |
| Compra entre 7 e 30 dias | Clientes que compraram na empresa nos últimos 30 dias, há pelo menos 7 dias sem comprar, sem rota nos últimos 7 dias, com pelo menos 5% do limite de crédito | 14 dias | Times paola_1 e paola_2; segunda a sábado; também considera recência no grupo (nunca compraram ou mais de 7 dias) |
| Compra entre 31 e 60 dias | Clientes que compraram na empresa nos últimos 60 dias, há mais de 30 dias sem comprar, sem rota nos últimos 7 dias, com pelo menos 5% do limite de crédito | 14 dias | Times paola_1 e paola_2; preferência segunda a sábado |
| Compra entre 61 e 89 dias | Clientes que compraram na empresa nos últimos 89 dias, há mais de 60 dias sem comprar, sem rota nos últimos 7 dias, com pelo menos 5% do limite de crédito | 7 dias | Times paola_1 e paola_2; preferência segunda a sábado |
| Compra entre 90 e 179 dias | Clientes que compraram na empresa nos últimos 179 dias, há mais de 89 dias sem comprar, sem rota nos últimos 7 dias, com pelo menos 5% do limite de crédito | 14 dias | Times paola_1 e paola_2; preferência segunda a sábado |
| Sem compra em 180 dias | Clientes que nunca compraram, compraram nos últimos 6 dias ou estão há mais de 179 dias sem comprar, sem rota nos últimos 7 dias, com 5% ou mais de crédito | 21 dias | Times paola_1 e paola_2; preferência segunda a sábado; no grupo, nunca compraram ou há mais de 7 dias sem comprar |
| Demais clientes | Clientes do temporario_2meses sem rota há 14 dias ou com menos de 5% de crédito, e de paola_1/paola_2 com menos de 5% e sem comprar há mais de 7 dias | Não agendar | Regra final: vale para quem sobrou das faixas anteriores; nos times paola inclui quem nunca comprou |

## Pontos de atenção

- As regras misturam recência de compra medida na empresa toda ('Clientes com compra entre 7 e 30 dias', 'Clientes com compra entre 31 e 60 dias' e 'Clientes com compra entre 61 e 89 dias') e no grupo de vendedores ('Nao agendar - clientes com recencia de positivacao em 7 dias', 'Clientes com compra em 30 dias' e 'Clientes com compra entre 30 e 90 dias'); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
