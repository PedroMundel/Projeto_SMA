# regra_169.gobr

Regra dos times televendas e televendas_2 por tempo desde a última compra: prospects e faixas de até 30, 60, 90 e 180 dias, todas a cada 14 dias, aplicadas à segmentação de ruptura de fornecedor e à carteira televendas consumidor. Deixam de ser agendados os clientes com compra em 7 dias, os inadimplentes e os com choque de agendas. O time televendas_2 tem ainda uma regra final de frequência para quem nunca comprou ou está há mais de 7 dias sem comprar.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas consumidor | Carteira fixa dos vendedores do time televendas com clientes adimplentes que nunca compraram ou estão há mais de 7 dias sem comprar, fora da segmentação televendas ruptura de fornecedor |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos até 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos de 30 a 60 dias | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Ativos de 60 a 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Inativos | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 14 dias | Vale para a segmentação de ruptura de fornecedor e para a carteira televendas consumidor |
| Bloqueio: compra em 7 dias | Clientes dos times televendas e televendas_2 que compraram nos últimos 7 dias, exceto os do televendas que estão na carteira consumidor e na segmentação de ruptura | Não agendar | Executada depois das faixas de frequência |
| Bloqueio: inadimplentes | Clientes inadimplentes, exceto os já tratados pelas regras anteriores | Não agendar | Executada depois das faixas de frequência; vale para os times televendas e televendas_2 |
| Bloqueio: choque de agendas | Clientes que nunca compraram ou estão há mais de 7 dias sem comprar, fora da segmentação de ruptura ou da carteira consumidor; nas duas, só acima de 180 dias | Não agendar | Vale para o time televendas, exceto os já tratados pelas regras anteriores |
| Televendas_2 sem venda recente | Clientes do time televendas_2 que nunca compraram ou estão há mais de 7 dias sem comprar | 14 dias | Regra final do time televendas_2 |

## Pontos de atenção

- O nome da regra 'Ativos com compra entre 7d e 30d' fala em 7 dias, mas a regra usa outro valor.
- O bloqueio 'Ativos com compra em 7 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Ativos com compra entre 7d e 30d'.
- O bloqueio 'Não agendar Inadimplentes' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Clientes Prospects', 'Ativos com compra entre 7d e 30d', 'Ativos com compra entre 30d e 60d', 'Ativos com compra entre 60d e 90d' e 'Clientes inativos'.
