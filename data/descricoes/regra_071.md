# regra_071.gobr

Regras de frequência para cinco grupos de atendimento: televendas do PI e do PB (carteiras próprias), vendedores do Tocantins, time de televendas e time de campo. Nos grupos de televendas, inadimplentes inativos têm frequência fixa (14 dias; 30 dias no time de televendas) e os demais seguem o histórico de visitas, com máximo de 7 dias. O time de campo atende todos os clientes a cada 7 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas pi | Carteira fixa dos vendedores do time televendas pi |
| carteira televendas pb | Carteira fixa dos vendedores do time televendas pb |
| carteira tocantins | Carteira fixa dos vendedores do time tocantins |
| carteira televendas | Carteira fixa dos vendedores do time de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos inadimplentes (PI e PB) | Clientes inadimplentes e inativos para o vendedor, nas carteiras televendas pi e televendas pb | 14 dias | Preferência de segunda a sexta; sem choque com os dias do time campo (roteirizáveis) |
| Demais clientes (PI) | Clientes da carteira televendas pi que não são inativos para o vendedor, ou que são inativos e adimplentes | Pelo histórico, no máximo 7 dias | Preferência de segunda a sábado; sem choque com os dias do time campo (roteirizáveis) |
| Demais clientes (PB) | Clientes da carteira televendas pb que não são inativos para o vendedor, ou que são inativos e adimplentes | Pelo histórico, no máximo 7 dias | Preferência de segunda a sexta; sem choque com os dias do time campo (roteirizáveis) |
| Inativos inadimplentes (Tocantins) | Clientes inadimplentes e inativos para o vendedor da carteira tocantins | 14 dias | Preferência de segunda a sexta; sem choque com os dias do time campo (roteirizáveis) |
| Demais clientes (Tocantins) | Clientes da carteira tocantins que não são inativos para o vendedor, ou que são inativos e adimplentes | Pelo histórico, no máximo 7 dias | Preferência de segunda a sábado; sem choque com os dias do time campo (roteirizáveis) |
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor do time televendas | Pelo histórico, no máximo 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor do time televendas | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor do time televendas | Pelo histórico, no máximo 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor do time televendas | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Sem vendas (televendas) | Clientes sem vendas para o vendedor do time televendas | Pelo histórico, no máximo 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Todos os clientes (campo) | Todos os clientes do time campo | 7 dias | Frequência semanal |

## Pontos de atenção

- Várias combinações de clientes das carteiras televendas pi e televendas pb não se enquadram em nenhuma regra e ficam sem parametrização.
