# regra_169.gobr

Regra para dois times de televendas. Os clientes da carteira televendas consumidor e da segmentação de ruptura de fornecedor entram em cinco faixas de 14 dias (prospects e compras em até 30, 60, 90 e 180 dias). Não são agendados os ativos com compra em 7 dias, os inadimplentes e os clientes em choque de agendas. O time televendas_2 tem uma regra final de 14 dias para quem não comprou nos últimos 7 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas consumidor | Carteira fixa dos vendedores do time televendas, com clientes adimplentes que nunca compraram ou estão há mais de 7 dias sem comprar, fora da segmentação de ruptura de fornecedor |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos até 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos de 30 a 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos de 60 a 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Inativos | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Bloqueio: ativos com compra em 7 dias | Clientes dos times televendas_2 e televendas que compraram nos últimos 7 dias; no televendas, só os de fora da carteira consumidor e da segmentação de ruptura | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes dos times televendas e televendas_2, exceto os já tratados pelas regras anteriores | Não agendar |  |
| Bloqueio: choque de agendas | Clientes do televendas que nunca compraram ou estão há mais de 7 dias sem comprar, fora da carteira e da segmentação; ou há mais de 180 dias sem comprar, nelas | Não agendar | A carteira é a televendas consumidor e a segmentação é a ruptura de fornecedor |
| Sem compra recente (televendas_2) | Clientes do time televendas_2 que nunca compraram ou estão há mais de 7 dias sem comprar | 14 dias |  |

## Pontos de atenção

- O bloqueio 'Ativos com compra em 7 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Ativos com compra entre 7d e 30d'.
- O bloqueio 'Não agendar Inadimplentes' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Clientes Prospects', 'Ativos com compra entre 7d e 30d', 'Ativos com compra entre 30d e 60d', 'Ativos com compra entre 60d e 90d' e 'Clientes inativos'.
