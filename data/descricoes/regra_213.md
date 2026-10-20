# regra_213.gobr

Regra de atendimento do time televendas dividida em seis carteiras fixas por código de rota, uma para cada dia da semana (segunda a sexta) mais Curitiba. Nas carteiras de segunda a sexta, clientes ativos para o vendedor têm frequência semanal de 7 dias e os não ativos de 28 dias, sempre com preferência no dia da carteira e parametrização fixa. Clientes filiais não são agendados. A carteira de Curitiba tem uma regra única, de 7 dias para todos os clientes.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira_segunda | Carteira fixa dos vendedores do time televendas, com clientes das rotas 24, 523, 524, 525 e 526 |
| carteira_terca | Carteira fixa dos vendedores do time televendas, com clientes das rotas 17, 3, 4, 500, 512, 514 e mais 1, exceto os já alocados em carteira_segunda |
| carteira_quarta | Carteira fixa dos vendedores do time televendas, com clientes das rotas 502, 530 e 531, exceto os já alocados em carteira_segunda e carteira_terca |
| carteira_quinta | Carteira fixa dos vendedores do time televendas, com clientes das rotas 20, 501, 504, 505, 506, 508 e mais 4, exceto os já alocados nas carteiras de segunda a quarta |
| carteira_sexta | Carteira fixa dos vendedores do time televendas, com clientes das rotas 19, 5, 510, 511 e 521, exceto os já alocados nas carteiras de segunda a quinta |
| carteira_curitiba | Carteira fixa dos vendedores do time televendas, com clientes das rotas 10 e 11, exceto os já alocados nas carteiras de segunda a sexta |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativos (segunda) | Clientes ativos para o vendedor da carteira de segunda | 7 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Inativos (segunda) | Clientes não ativos para o vendedor da carteira de segunda | 28 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Ativos (terça) | Clientes ativos para o vendedor da carteira de terça | 7 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Inativos (terça) | Clientes não ativos para o vendedor da carteira de terça | 28 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Ativos (quarta) | Clientes ativos para o vendedor da carteira de quarta | 7 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Inativos (quarta) | Clientes não ativos para o vendedor da carteira de quarta | 28 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Ativos (quinta) | Clientes ativos para o vendedor da carteira de quinta | 7 dias | Preferência: quinta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Inativos (quinta) | Clientes não ativos para o vendedor da carteira de quinta | 28 dias | Preferência: quinta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Ativos (sexta) | Clientes ativos para o vendedor da carteira de sexta | 7 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Inativos (sexta) | Clientes não ativos para o vendedor da carteira de sexta | 28 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Sem dia específico (Curitiba) | Todos os clientes da carteira de Curitiba | 7 dias |  |

## Pontos de atenção

- Clientes do time televendas que estão fora das carteiras carteira_curitiba, carteira_quarta, carteira_quinta, carteira_segunda, carteira_sexta e carteira_terca não se enquadram em nenhuma regra e ficam sem parametrização.
