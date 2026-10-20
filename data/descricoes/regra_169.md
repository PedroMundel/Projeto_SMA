# regra_169.gobr

Regra de agendamento dos times de televendas por tempo desde a última compra, em faixas de até 30, 60, 90 e 180 dias mais os prospects, todas com frequência de 14 dias, para a carteira televendas consumidor e a segmentação de ruptura de fornecedor. O time televendas_2 tem ainda uma regra própria de 14 dias para quem nunca comprou ou está há mais de 7 dias sem comprar. Deixam de ser agendados os ativos com compra em 7 dias, os inadimplentes e os clientes em choque de agendas.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas consumidor | Carteira fixa dos vendedores de televendas, com clientes adimplentes que nunca compraram ou estão há mais de 7 dias sem comprar, fora da segmentação de ruptura de fornecedor |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos até 30 dias | Clientes que compraram nos últimos 30 dias | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos entre 30 e 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos entre 60 e 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Clientes inativos | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Bloqueio: ativos com compra em 7 dias | Clientes que compraram nos últimos 7 dias: do time televendas_2, ou do televendas fora da carteira televendas consumidor e da segmentação de ruptura de fornecedor | Não agendar | Vale para os times televendas e televendas_2 |
| Bloqueio: inadimplentes | Clientes inadimplentes, exceto os já tratados pelas regras anteriores | Não agendar | Vale para os times televendas e televendas_2 |
| Bloqueio: choque de agendas | Clientes que nunca compraram ou estão há mais de 7 dias sem comprar, fora da carteira consumidor e da segmentação de ruptura; ou com mais de 180 dias sem comprar | Não agendar | Vale para o time televendas |
| Sem venda recente (televendas_2) | Clientes do time televendas_2 que nunca compraram ou estão há mais de 7 dias sem comprar | 14 dias | Vale para o time televendas_2 |

## Pontos de atenção

- O nome da regra 'Ativos com compra entre 7d e 30d' fala em 7 dias, mas a regra usa outro valor: ela considera quem comprou nos últimos 30 dias.
- O bloqueio 'Ativos com compra em 7 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Ativos com compra entre 7d e 30d'.
- O bloqueio 'Não agendar Inadimplentes' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Clientes Prospects', 'Ativos com compra entre 7d e 30d', 'Ativos com compra entre 30d e 60d', 'Ativos com compra entre 60d e 90d' e 'Clientes inativos'.
