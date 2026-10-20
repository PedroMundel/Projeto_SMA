# regra_174.gobr

Regra de agendamento do time de televendas, organizada pela situação do cliente com o próprio vendedor: potenciais, recém-ativados, ativos, em ruptura e inativos. Deixam de ser agendados os inadimplentes e os clientes baixados na Receita Federal. Parte das faixas de ativos usa a frequência calculada pelo histórico, e os ramos de atividade 18 e 9 têm faixas próprias. A última regra reativa quem está há mais de 90 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativados com uma única compra | Clientes que já compraram com o próprio vendedor, cadastrados no ERP há pelo menos 60 dias e com uma única compra com ele | 21 dias |  |
| Ativos de alta frequência | Clientes que compraram com o próprio vendedor nos últimos 30 dias, com frequência histórica de compra de menos de 14 dias | Pelo histórico, entre 10 e 14 dias | Frequência calculada pelo histórico, limitada a no mínimo 10 e no máximo 14 dias |
| Ativos que compram regularmente (ramos 18 e 9) | Clientes dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, com frequência histórica de menos de 30 dias, exceto os já tratados antes | Pelo histórico, entre 14 e 21 dias | Frequência calculada pelo histórico, limitada a no mínimo 14 e no máximo 21 dias |
| Ativos que compram regularmente (outros ramos) | Clientes fora dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, com frequência histórica de menos de 30 dias, exceto os já tratados antes | 28 dias |  |
| Ativos a estimular (ramos 18 e 9) | Clientes dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar | 14 dias | Frequência histórica indefinida ou de pelo menos 30 dias; compra única só se cadastrado há menos de 60 dias |
| Ativos a estimular (outros ramos) | Clientes fora dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar | 21 dias | Frequência histórica indefinida ou de pelo menos 30 dias; compra única só se cadastrado há menos de 60 dias |
| Em ruptura (ramos 9 e 18) | Clientes dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Compra única só se cadastrado no ERP há menos de 60 dias |
| Em ruptura (outros ramos) | Clientes fora dos ramos 18 e 9 que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Compra única só se cadastrado no ERP há menos de 60 dias |
| Inativos | Clientes que estão há mais de 90 dias sem comprar com o próprio vendedor | 21 dias | Regra final; compra única só se cadastrado no ERP há menos de 60 dias |

## Pontos de atenção

- A condição da regra 'Ativo: compra regularmente' (frequência de 14 a 21 dias pelo histórico) é complexa demais para resumir e foi descrita pelo critério próprio, exceto os clientes já tratados pelas regras anteriores.
- A condição da regra 'Ativo: compra regularmente' (frequência de 28 dias) é complexa demais para resumir e foi descrita pelo critério próprio, exceto os clientes já tratados pelas regras anteriores.
- Clientes que compraram com o próprio vendedor nos últimos 20 dias e têm frequência histórica indefinida ou de pelo menos 30 dias não se enquadram em nenhuma regra e ficam sem parametrização.
