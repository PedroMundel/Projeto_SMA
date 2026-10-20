# regra_182.gobr

Regra de agendamento do time de televendas, organizada por ramo de atividade. Não são agendados pessoas físicas, inadimplentes, clientes baixados na Receita Federal e clientes que compraram nos últimos 7 dias. Os prospects de quinze ramos têm frequência única, e cada ramo tem duas faixas conforme o tempo desde o último pedido, com prazos próprios por ramo. Clientes de ramos fora dessa lista ficam sem parametrização.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: CPF | Clientes pessoa física | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: pedido nos últimos 7 dias | Clientes que compraram nos últimos 7 dias | Não agendar |  |
| Prospects dos ramos 89 a 103 | Clientes que nunca compraram com qualquer vendedor da empresa, dos ramos de atividade 089, 090, 091, 092, 093, 094 e mais 9 | 7 dias |  |
| Mangueiras com pedido em 45 dias | Clientes do ramo de atividade 089 que compraram nos últimos 45 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Mangueiras com pedido acima de 45 dias | Clientes do ramo de atividade 089 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 45 dias sem comprar nele | 7 dias |  |
| Materiais de limpeza com pedido em 60 dias | Clientes do ramo de atividade 090 que compraram nos últimos 60 dias, mas estão há mais de 7 dias sem comprar | 21 dias |  |
| Materiais de limpeza com pedido acima de 60 dias | Clientes do ramo de atividade 090 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 60 dias sem comprar nele | 10 dias |  |
| Revenda EPI com pedido em 45 dias | Clientes do ramo de atividade 091 que compraram nos últimos 45 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Revenda EPI com pedido acima de 45 dias | Clientes do ramo de atividade 091 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 45 dias sem comprar nele | 7 dias |  |
| Materiais de construção com pedido em 90 dias | Clientes do ramo de atividade 092 que compraram nos últimos 90 dias, mas estão há mais de 7 dias sem comprar | 28 dias |  |
| Materiais de construção com pedido acima de 90 dias | Clientes do ramo de atividade 092 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 14 dias |  |
| Ferragem e ferramentas com pedido em 45 dias | Clientes do ramo de atividade 093 que compraram nos últimos 45 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Ferragem e ferramentas com pedido acima de 45 dias | Clientes do ramo de atividade 093 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 45 dias sem comprar nele | 7 dias |  |
| Agropecuária com pedido em 90 dias | Clientes do ramo de atividade 094 que compraram nos últimos 90 dias, mas estão há mais de 7 dias sem comprar | 28 dias |  |
| Agropecuária com pedido acima de 90 dias | Clientes do ramo de atividade 094 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 14 dias |  |
| Prestador de serviço com pedido em 75 dias | Clientes do ramo de atividade 095 que compraram nos últimos 75 dias, mas estão há mais de 7 dias sem comprar | 21 dias |  |
| Prestador de serviço com pedido acima de 75 dias | Clientes do ramo de atividade 095 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 75 dias sem comprar nele | 14 dias |  |
| Indústria com pedido em 75 dias | Clientes do ramo de atividade 096 que compraram nos últimos 75 dias, mas estão há mais de 7 dias sem comprar | 28 dias |  |
| Indústria com pedido acima de 75 dias | Clientes do ramo de atividade 096 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 75 dias sem comprar nele | 14 dias |  |
| Cooperativa com pedido em 60 dias | Clientes do ramo de atividade 097 que compraram nos últimos 60 dias, mas estão há mais de 7 dias sem comprar | 21 dias |  |
| Cooperativa com pedido acima de 60 dias | Clientes do ramo de atividade 097 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 60 dias sem comprar nele | 10 dias |  |
| Home center com pedido em 60 dias | Clientes do ramo de atividade 098 que compraram nos últimos 60 dias, mas estão há mais de 7 dias sem comprar | 21 dias |  |
| Home center com pedido acima de 60 dias | Clientes do ramo de atividade 098 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 60 dias sem comprar nele | 10 dias |  |
| Atacado com pedido em 45 dias | Clientes do ramo de atividade 099 que compraram nos últimos 45 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Atacado com pedido acima de 45 dias | Clientes do ramo de atividade 099 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 45 dias sem comprar nele | 7 dias |  |
| Construtora com pedido em 75 dias | Clientes do ramo de atividade 100 que compraram nos últimos 75 dias, mas estão há mais de 7 dias sem comprar | 28 dias |  |
| Construtora com pedido acima de 75 dias | Clientes do ramo de atividade 100 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 75 dias sem comprar nele | 7 dias |  |
| Órgão público com pedido em 90 dias | Clientes do ramo de atividade 101 que compraram nos últimos 90 dias, mas estão há mais de 7 dias sem comprar | 28 dias |  |
| Órgão público com pedido acima de 90 dias | Clientes do ramo de atividade 101 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 14 dias |  |
| E-commerce com pedido em 45 dias | Clientes do ramo de atividade 102 que compraram nos últimos 45 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| E-commerce com pedido acima de 45 dias | Clientes do ramo de atividade 102 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 45 dias sem comprar nele | 7 dias |  |
| Produtor rural com pedido em 90 dias | Clientes do ramo de atividade 103 que compraram nos últimos 90 dias, mas estão há mais de 7 dias sem comprar | 28 dias |  |
| Produtor rural com pedido acima de 90 dias | Clientes do ramo de atividade 103 que já compraram com algum vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 14 dias |  |

## Pontos de atenção

- Clientes de ramos de atividade fora de 089, 090, 091, 092, 093, 094 e mais 9 não se enquadram em nenhuma regra e ficam sem parametrização.
