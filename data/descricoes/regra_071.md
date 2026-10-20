# regra_071.gobr

Regras de frequência por região e time: televendas PI, televendas PB, Tocantins, televendas geral e campo. Inativos inadimplentes têm frequência de 14 dias nas carteiras de PI, PB e Tocantins e de 30 dias no televendas geral; os demais clientes seguem o histórico de compras, limitado a no máximo 7 dias quando não há histórico. O time de campo atende todos os clientes a cada 7 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas pi | Carteira fixa dos vendedores do time televendas pi |
| carteira televendas pb | Carteira fixa dos vendedores do time televendas pb |
| carteira tocantins | Carteira fixa dos vendedores do time tocantins |
| carteira televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos inadimplentes (PI e PB) | Clientes inadimplentes e inativos para o vendedor | 14 dias | Carteiras televendas pi e pb; atendimento de segunda a sexta; evita dias do time campo (só roteirizáveis) |
| Demais clientes (PI) | Clientes que não são inativos para o vendedor ou que são adimplentes e inativos | Pelo histórico de compras; sem histórico, no máximo 7 dias | Carteira televendas pi; atendimento de segunda a sábado; evita dias do time campo (só roteirizáveis) |
| Demais clientes (PB) | Clientes que não são inativos para o vendedor ou que são adimplentes e inativos | Pelo histórico de compras; sem histórico, no máximo 7 dias | Carteira televendas pb; atendimento de segunda a sexta; evita dias do time campo (só roteirizáveis) |
| Inativos inadimplentes (Tocantins) | Clientes inadimplentes e inativos para o vendedor | 14 dias | Carteira tocantins; atendimento de segunda a sexta; evita dias do time campo (só roteirizáveis) |
| Demais clientes (Tocantins) | Clientes que não são inativos para o vendedor ou que são adimplentes e inativos | Pelo histórico de compras; sem histórico, no máximo 7 dias | Carteira tocantins; atendimento de segunda a sábado; evita dias do time campo (só roteirizáveis) |
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor | Pelo histórico de compras; sem histórico, no máximo 7 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor | 14 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | Pelo histórico de compras; sem histórico, no máximo 7 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | 30 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor | Pelo histórico de compras; sem histórico, no máximo 7 dias | Atendimento de segunda a sexta; demais dias sem atendimento |
| Todos os clientes (campo) | Todos os clientes do time de campo | 7 dias |  |

## Pontos de atenção

- Nas carteiras televendas pi e televendas pb, várias combinações de clientes não se enquadram em nenhuma regra e ficam sem parametrização.
