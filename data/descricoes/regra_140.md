# regra_140.gobr

Regra de agendamento do time de televendas organizada por carteiras de rotas: rotas de dias variáveis, rotas 3 e 4, rota 5, rota 6 e rota 7. Em cada carteira há cinco faixas de frequência semanal (7 dias), da primeira compra até clientes sem compra há mais de 90 dias. Não são agendados pessoa física, filiais, inadimplentes e clientes visitados nos últimos 3 dias. Clientes sem rota associada caem na regra final, também semanal.

## Carteiras

| Carteira | Descrição |
|---|---|
| rotas_dias_variaveis | Carteira fixa dos vendedores de televendas com clientes das rotas 10, 11, 8 e 9 |
| rotas 3 e 4 | Carteira fixa dos vendedores de televendas com clientes das rotas 3 e 4, exceto os já alocados em rotas_dias_variaveis |
| rota 5 | Carteira fixa dos vendedores de televendas com clientes da rota 5, exceto os já alocados nas carteiras anteriores |
| rota 6 | Carteira fixa dos vendedores de televendas com clientes da rota 6, exceto os já alocados nas carteiras anteriores |
| rota 7 | Carteira fixa dos vendedores de televendas com clientes da rota 7, exceto os já alocados nas carteiras anteriores |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: visita recente | Clientes das carteiras de rotas que foram visitados nos últimos 3 dias | Não agendar |  |
| Rotas dias variáveis: primeira compra | Clientes sem vendas para o vendedor | 7 dias |  |
| Rotas dias variáveis: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias | 7 dias |  |
| Rotas dias variáveis: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, mas estão há pelo menos 21 dias sem comprar e há mais de 21 dias sem comprar com o próprio vendedor | 7 dias |  |
| Rotas dias variáveis: risco de inatividade | Clientes com venda para o vendedor que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar | 7 dias |  |
| Rotas dias variáveis: sem compra há mais de 90 dias | Clientes com venda para o vendedor que estão há mais de 90 dias sem comprar | 7 dias |  |
| Rotas 3 e 4: primeira compra | Clientes sem vendas para o vendedor | 7 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rotas 3 e 4: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias | 7 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rotas 3 e 4: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, mas estão há pelo menos 21 dias sem comprar e há mais de 21 dias sem comprar com o próprio vendedor | 7 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rotas 3 e 4: risco de inatividade | Clientes com venda para o vendedor que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar | 7 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rotas 3 e 4: sem compra há mais de 90 dias | Clientes com venda para o vendedor que estão há mais de 90 dias sem comprar | 7 dias | Preferência: segunda; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 5: primeira compra | Clientes sem vendas para o vendedor | 7 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 5: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias | 7 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 5: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, mas estão há pelo menos 21 dias sem comprar e há mais de 21 dias sem comprar com o próprio vendedor | 7 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 5: risco de inatividade | Clientes com venda para o vendedor que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar | 7 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 5: sem compra há mais de 90 dias | Clientes com venda para o vendedor que estão há mais de 90 dias sem comprar | 7 dias | Preferência: terça; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 6: primeira compra | Clientes sem vendas para o vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 6: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias | 7 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 6: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, mas estão há pelo menos 21 dias sem comprar e há mais de 21 dias sem comprar com o próprio vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 6: risco de inatividade | Clientes com venda para o vendedor que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar | 7 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 6: sem compra há mais de 90 dias | Clientes com venda para o vendedor que estão há mais de 90 dias sem comprar | 7 dias | Preferência: quarta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 7: primeira compra | Clientes sem vendas para o vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 7: compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 21 dias | 7 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 7: estimular regularidade | Clientes que compraram no grupo de vendedores nos últimos 41 dias, mas estão há pelo menos 21 dias sem comprar e há mais de 21 dias sem comprar com o próprio vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 7: risco de inatividade | Clientes com venda para o vendedor que compraram nos últimos 90 dias, mas estão há mais de 41 dias sem comprar | 7 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Rota 7: sem compra há mais de 90 dias | Clientes com venda para o vendedor que estão há mais de 90 dias sem comprar | 7 dias | Preferência: sexta; demais dias sem atendimento. Parametrização fixa (restrição rígida de frequência e dias) |
| Clientes sem rotas associadas | Clientes fora das carteiras de rotas, ou de rota com compra no grupo nos últimos 20 dias e mais de 21 dias sem comprar com o vendedor | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- As faixas misturam escopos de tempo sem compra (grupo de vendedores e próprio vendedor), então podem se sobrepor ou deixar clientes sem faixa.
- O arquivo contém caracteres de controle invisíveis, possível erro de digitação.
