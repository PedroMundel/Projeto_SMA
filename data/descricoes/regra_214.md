# regra_214.gobr

Regra do time de televendas por situação do cliente com o vendedor, com frequências de 10, 14, 21 e 30 dias e atendimento de segunda a sábado. Inadimplentes não são agendados. Clientes com uma única compra entram primeiro numa faixa de 14 dias; os demais são divididos por regularidade de compra, tempo sem comprar e ramo de atividade 29.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Cliente sem pedido com o vendedor | Clientes com uma única compra com o vendedor | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Ativado, ramo 29 | Clientes do ramo de atividade 29 que compraram nos últimos 30 dias e têm uma única compra com o vendedor | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Preferência: segunda a sábado |
| Ativado, outros ramos | Clientes de ramo de atividade diferente de 29 que compraram nos últimos 30 dias e têm uma única compra com o vendedor | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Preferência: segunda a sábado |
| Ativo: compra regularmente | Clientes ativos para o vendedor, com frequência histórica de compra de menos de 14 dias e mais de uma compra com o vendedor | 10 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Estimular regularidade, ramo 29 | Clientes do ramo de atividade 29, com mais de uma compra com o vendedor, que compraram com ele nos últimos 59 dias, mas estão há pelo menos 21 dias sem comprar | 30 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Estimular regularidade, outros ramos | Clientes de ramo diferente de 29, com mais de uma compra com o vendedor, que compraram com ele nos últimos 59 dias, mas estão há pelo menos 21 dias sem comprar | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Em ruptura, ramo 29 | Clientes do ramo de atividade 29, com mais de uma compra com o vendedor, que compraram com ele nos últimos 89 dias, mas estão há mais de 59 dias sem comprar | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Em ruptura, outros ramos | Clientes de ramo diferente de 29, com mais de uma compra com o vendedor, que compraram com ele nos últimos 89 dias, mas estão há mais de 59 dias sem comprar | 14 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |
| Resgate de cliente sem compra | Clientes com mais de uma compra com o vendedor que estão há mais de 90 dias sem comprar com ele | 10 dias | Dias de preferência: segunda a sábado; demais dias sem atendimento |

## Pontos de atenção

- A regra 'Freq. de 21d para Ativado: fez um pedido e ainda não comprou mais' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Freq. de 14d para Ativado: fez um pedido e ainda não comprou mais' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- As faixas misturam medidas de tempo sem comprar de escopos diferentes (grupo de vendedores e vendedor), então podem se sobrepor ou deixar clientes sem regra.
- Clientes com mais de uma compra com o vendedor que compraram nos últimos 20 dias, ou que estão há mais de 89 dias sem comprar (tendo comprado nos últimos 90 dias), não se enquadram em nenhuma regra e ficam sem parametrização. O mesmo vale para quem nunca comprou com o vendedor e não é ativo para ele.
