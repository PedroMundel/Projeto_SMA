# regra_206.gobr

Regra de agendamento com dois times: ativo_inativo, que atende duas carteiras fixas por tempo desde a última compra (0_90 e 90_180), e prospeccao, que atende leads e prospects. Em cada grupo, a frequência varia conforme o ramo de atividade do cliente: três faixas por carteira ou time. Deixam de ser agendados filiais, inadimplentes e prospects do time ativo_inativo. A regra de ramos não especificados fecha cada grupo.

## Carteiras

| Carteira | Descrição |
|---|---|
| 0_90 | Carteira fixa dos vendedores do time ativo_inativo com clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias |
| 90_180 | Carteira fixa dos vendedores do time ativo_inativo com clientes que compraram com qualquer vendedor da empresa nos últimos 180 dias, mas estão há pelo menos 91 dias sem comprar |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar | Vale para os times ativo_inativo e prospeccao |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar | Vale para os times ativo_inativo e prospeccao |
| Bloqueio: prospects | Clientes que nunca compraram com qualquer vendedor da empresa | Não agendar | Vale para o time ativo_inativo |
| Com pedido até 90 dias: ramos 1, 2, 4 e 12 | Clientes da carteira 0_90 com ramo de atividade (id) 1, 2, 4 ou 12 | 7 dias |  |
| Com pedido até 90 dias: ramo 3 | Clientes da carteira 0_90 com ramo de atividade (id) igual a 3 | 15 dias |  |
| Com pedido até 90 dias: demais ramos | Clientes da carteira 0_90 com ramo de atividade (id) fora de 1, 2, 3, 4 e 12 | 28 dias | Fecha a carteira 0_90 |
| Em risco, 90 a 180 dias: ramos 1, 2, 4 e 12 | Clientes da carteira 90_180 com ramo de atividade (id) 1, 2, 4 ou 12 | 7 dias |  |
| Em risco, 90 a 180 dias: ramo 3 | Clientes da carteira 90_180 com ramo de atividade (id) igual a 3 | 15 dias |  |
| Em risco, 90 a 180 dias: demais ramos | Clientes da carteira 90_180 com ramo de atividade (id) fora de 1, 2, 3, 4 e 12 | 28 dias | Fecha a carteira 90_180 |
| Prospecção: ramos 1, 2, 4 e 12 | Clientes do time prospeccao com ramo de atividade (id) 1, 2, 4 ou 12 | 7 dias |  |
| Prospecção: ramo 3 | Clientes do time prospeccao com ramo de atividade (id) igual a 3 | 15 dias |  |
| Prospecção: demais ramos | Clientes do time prospeccao com ramo de atividade (id) fora de 1, 2, 3, 4 e 12 | 28 dias | Regra final do time prospeccao |

## Pontos de atenção

- O nome da regra 'Com pedido nos últimos 90d dos segmentos POSTO DE MOLAS, EMPRESA ÔNIBUS, AUTO PEÇAS e MINERAÇÃO' fala em 90 dias, mas a regra usa outro valor.
- O nome da regra 'Com pedido nos últimos 90d do segmento TRANSPORTADORA' fala em 90 dias, mas a regra usa outro valor.
- O nome da regra 'Com pedido nos últimos 90d de segmentos não especificados' fala em 90 dias, mas a regra usa outro valor.
- O nome da regra 'Com pedido entre 90d e 180d (clientes em risco) dos segmentos POSTO DE MOLAS, EMPRESA ÔNIBUS, AUTO PEÇAS e MINERAÇÃO' fala em 90 e 180 dias, mas a regra usa outros valores.
- O nome da regra 'Com pedido entre 90d e 180d (clientes em risco) do segmento TRANSPORTADORA' fala em 90 e 180 dias, mas a regra usa outros valores.
- O nome da regra 'Com pedido entre 90d e 180d (clientes em risco) de segmentos não especificados' fala em 90 e 180 dias, mas a regra usa outros valores.
- Clientes dos times ativo_inativo e prospeccao que estão fora das carteiras 0_90 e 90_180 não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes do time ativo_inativo que estão fora das carteiras 0_90 e 90_180 não se enquadram em nenhuma regra e ficam sem parametrização.
