# regra_206.gobr

Planejamento de dois times: ativo_inativo, que atende duas carteiras fixas por tempo desde a última compra (0_90 e 90_180), e prospeccao, que atende leads e prospects. Em todas as faixas a frequência depende do ramo de atividade: 7, 15 ou 28 dias. Não são agendadas filiais e inadimplentes (nos dois times), nem prospects no time ativo_inativo.

## Carteiras

| Carteira | Descrição |
|---|---|
| 0_90 | Carteira fixa dos vendedores do time ativo_inativo com clientes que compraram na empresa nos últimos 90 dias |
| 90_180 | Carteira fixa dos vendedores do time ativo_inativo com clientes que compraram na empresa nos últimos 180 dias, mas estão há pelo menos 91 dias sem comprar |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: prospects | Clientes que nunca compraram na empresa | Não agendar | Vale só para o time ativo_inativo |
| 0_90: posto de molas, ônibus, auto peças e mineração | Clientes da carteira 0_90 com ramo de atividade (id) 1, 12, 2 ou 4 | 7 dias |  |
| 0_90: transportadora | Clientes da carteira 0_90 com ramo de atividade (id) 3 | 15 dias |  |
| 0_90: demais segmentos | Clientes da carteira 0_90 com ramo de atividade (id) diferente de 1, 12, 2, 3 e 4 | 28 dias |  |
| 90_180: posto de molas, ônibus, auto peças e mineração | Clientes da carteira 90_180 com ramo de atividade (id) 1, 12, 2 ou 4 | 7 dias |  |
| 90_180: transportadora | Clientes da carteira 90_180 com ramo de atividade (id) 3 | 15 dias |  |
| 90_180: demais segmentos | Clientes da carteira 90_180 com ramo de atividade (id) diferente de 1, 12, 2, 3 e 4 | 28 dias |  |
| Prospecção: posto de molas, ônibus, auto peças e mineração | Clientes do time prospeccao com ramo de atividade (id) 1, 12, 2 ou 4 | 7 dias |  |
| Prospecção: transportadora | Clientes do time prospeccao com ramo de atividade (id) 3 | 15 dias |  |
| Prospecção: demais segmentos | Clientes do time prospeccao com ramo de atividade (id) diferente de 1, 12, 2, 3 e 4 | 28 dias | Regra final do time prospeccao |

## Pontos de atenção

- Clientes do time ativo_inativo e do time prospeccao que estão fora das carteiras 0_90 e 90_180 não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes do time ativo_inativo que estão fora das carteiras 0_90 e 90_180 não se enquadram em nenhuma regra e ficam sem parametrização.
