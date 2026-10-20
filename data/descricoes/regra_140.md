# regra_140.gobr

Regra de agendamento do time de televendas organizada por carteiras de rotas: uma de rotas em dias variáveis (10, 11, 8 e 9) e quatro de rotas fixas (3 e 4 na segunda, 5 na terça, 6 na quarta e 7 na sexta). Em cada carteira há cinco faixas por histórico de compra (primeira compra, compra regularmente, estimular a regularidade, risco de inatividade e sem compra há mais de 90 dias), todas com frequência de 7 dias. Deixam de ser agendados os clientes pessoa física, as filiais, os inadimplentes e os visitados nos últimos 3 dias. A regra final atende com 7 dias os clientes sem rota associada.

## Carteiras

| Carteira | Descrição |
|---|---|
| rotas_dias_variaveis | Carteira fixa dos vendedores de televendas com clientes das rotas 10, 11, 8 e 9 |
| rotas 3 e 4 | Carteira fixa dos vendedores de televendas com clientes das rotas 3 e 4, exceto os já alocados em rotas_dias_variaveis |
| rota 5 | Carteira fixa dos vendedores de televendas com clientes da rota 5, exceto os já alocados em rotas_dias_variaveis e rotas 3 e 4 |
| rota 6 | Carteira fixa dos vendedores de televendas com clientes da rota 6, exceto os já alocados em rotas_dias_variaveis, rotas 3 e 4 e rota 5 |
| rota 7 | Carteira fixa dos vendedores de televendas com clientes da rota 7, exceto os já alocados em rotas_dias_variaveis, rotas 3 e 4, rota 5 e rota 6 |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: visita recente | Clientes das carteiras de rotas que foram visitados nos últimos 3 dias | Não agendar | Vale para as cinco carteiras de rotas |
| Rotas dias variáveis: primeira compra | Clientes da carteira de rotas em dias variáveis sem vendas para o vendedor | 7 dias |  |
| Rotas dias variáveis: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias e têm alguma venda (ativos ou inativos) para o vendedor | 7 dias |  |
| Rotas dias variáveis: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, sem comprar há pelo menos 21 dias, e há mais de 21 dias sem comprar com o vendedor | 7 dias | Inclui quem nunca comprou com o vendedor; exige alguma venda para o vendedor |
| Rotas dias variáveis: risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias |  |
| Rotas dias variáveis: sem compra há mais de 90 dias | Clientes há mais de 90 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias |  |
| Rotas 3 e 4: primeira compra | Clientes da carteira das rotas 3 e 4 sem vendas para o vendedor | 7 dias | Preferência: segunda; demais dias sem atendimento; parametrização fixa |
| Rotas 3 e 4: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias e têm alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: segunda; demais dias sem atendimento; parametrização fixa |
| Rotas 3 e 4: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, sem comprar há pelo menos 21 dias, e há mais de 21 dias sem comprar com o vendedor | 7 dias | Preferência: segunda; fixo. Inclui quem nunca comprou com o vendedor; exige alguma venda para ele |
| Rotas 3 e 4: risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: segunda; demais dias sem atendimento; parametrização fixa |
| Rotas 3 e 4: sem compra há mais de 90 dias | Clientes há mais de 90 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: segunda; demais dias sem atendimento; parametrização fixa |
| Rota 5: primeira compra | Clientes da carteira da rota 5 sem vendas para o vendedor | 7 dias | Preferência: terça; demais dias sem atendimento; parametrização fixa |
| Rota 5: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias e têm alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: terça; demais dias sem atendimento; parametrização fixa |
| Rota 5: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, sem comprar há pelo menos 21 dias, e há mais de 21 dias sem comprar com o vendedor | 7 dias | Preferência: terça; fixo. Inclui quem nunca comprou com o vendedor; exige alguma venda para ele |
| Rota 5: risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: terça; demais dias sem atendimento; parametrização fixa |
| Rota 5: sem compra há mais de 90 dias | Clientes há mais de 90 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: terça; demais dias sem atendimento; parametrização fixa |
| Rota 6: primeira compra | Clientes da carteira da rota 6 sem vendas para o vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento; parametrização fixa |
| Rota 6: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias e têm alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento; parametrização fixa |
| Rota 6: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, sem comprar há pelo menos 21 dias, e há mais de 21 dias sem comprar com o vendedor | 7 dias | Preferência: quarta; fixo. Inclui quem nunca comprou com o vendedor; exige alguma venda para ele |
| Rota 6: risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento; parametrização fixa |
| Rota 6: sem compra há mais de 90 dias | Clientes há mais de 90 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento; parametrização fixa |
| Rota 7: primeira compra | Clientes da carteira da rota 7 sem vendas para o vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento; parametrização fixa |
| Rota 7: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias e têm alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento; parametrização fixa |
| Rota 7: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, sem comprar há pelo menos 21 dias, e há mais de 21 dias sem comprar com o vendedor | 7 dias | Preferência: sexta; fixo. Inclui quem nunca comprou com o vendedor; exige alguma venda para ele |
| Rota 7: risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento; parametrização fixa |
| Rota 7: sem compra há mais de 90 dias | Clientes há mais de 90 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento; parametrização fixa |
| Clientes sem rota associada | Clientes sem rota associada ou, em rota, que nunca compraram no grupo ou compraram nos últimos 20 dias, e estão há mais de 21 dias sem comprar com o vendedor | 7 dias | Inclui quem nunca comprou com o vendedor; em rota, exige alguma venda para o vendedor |

## Pontos de atenção

- A sequência de regras mistura medidas de recência de compra (no grupo de vendedores e com o próprio vendedor) nas faixas de estimular a regularidade, risco de inatividade, sem compra há mais de 90 dias e compra regularmente; faixas de medidas diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- O arquivo contém caracteres de controle invisíveis, possível erro de digitação.
