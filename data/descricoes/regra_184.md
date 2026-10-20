# regra_184.gobr

Regra de agendamento de dois times. O time de televendas é organizado em sete faixas: compra única no mês atual e, por tempo sem comprar, até 7, 14, 30, 90, 180 dias e acima de 360 dias. O time São Paulo é organizado em cinco faixas pela frequência histórica de compra (7, 14, 28, 56 e 84 dias), com parametrização fixa e preferência pela segunda. Não há bloqueios; a regra final, de 30 dias, atende os clientes que não se enquadram nas demais.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Compra única no mês atual | Clientes com compra no mês atual e com uma única compra na empresa | 5 dias |  |
| Alta frequência de compra | Clientes que compraram nos últimos 7 dias, mas estão há pelo menos 1 dia sem comprar, exceto os já tratados antes | Pelo histórico; sem histórico, entre 1 e 5 dias | Dias de preferência: segunda e terça; demais dias sem atendimento |
| Manter regularidade | Clientes que compraram nos últimos 14 dias, mas estão há mais de 7 dias sem comprar, exceto os já tratados antes | Pelo histórico; sem histórico, entre 7 e 12 dias |  |
| Estimular compra no mês | Clientes que compraram nos últimos 30 dias, mas estão há mais de 14 dias sem comprar, exceto os já tratados antes | Pelo histórico; sem histórico, entre 14 e 28 dias |  |
| Gerar relacionamento | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados antes | 14 dias |  |
| Resgate de inativos | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, exceto os já tratados antes | 14 dias |  |
| Requalificar e ativar | Clientes que estão há mais de 360 dias sem comprar, exceto os já tratados antes | 21 dias |  |
| São Paulo: frequência semanal | Clientes do time São Paulo com frequência histórica de compra de 7 dias | 7 dias | Maior preferência: segunda; demais dias sem atendimento. Parametrização fixa, restrição rígida de frequência e dias |
| São Paulo: frequência quinzenal | Clientes do time São Paulo com frequência histórica de compra de 14 dias | 14 dias | Maior preferência: segunda; demais dias sem atendimento. Parametrização fixa, restrição rígida de frequência e dias |
| São Paulo: frequência mensal | Clientes do time São Paulo com frequência histórica de compra de 28 dias | 28 dias | Maior preferência: segunda; demais dias sem atendimento. Parametrização fixa, restrição rígida de frequência e dias |
| São Paulo: frequência bimestral | Clientes do time São Paulo com frequência histórica de compra de 56 dias | 56 dias | Maior preferência: segunda; demais dias sem atendimento. Parametrização fixa, restrição rígida de frequência e dias |
| São Paulo: frequência trimestral | Clientes do time São Paulo com frequência histórica de compra de 84 dias | 84 dias | Maior preferência: segunda; demais dias sem atendimento. Parametrização fixa, restrição rígida de frequência e dias |
| Demais clientes | Clientes do São Paulo (frequência indefinida ou fora de 7, 14, 28, 56 e 84 dias) e do televendas (nunca compraram, compraram hoje ou estão de 180 a 360 dias sem comprar) | 30 dias | Regra final: vale para quem sobrou das faixas anteriores |
