# regra_214.gobr

Regra de agendamento do time de televendas por tempo desde a última compra com o vendedor e por frequência histórica de compra, com faixas de 10, 14, 21 e 30 dias. Antes das faixas, deixam de ser agendados os inadimplentes. As faixas separam o ramo de atividade 29 dos demais, e duas faixas de clientes recém-ativados nunca são aplicadas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Compra única | Clientes com uma única compra com o vendedor | 14 dias | Preferência: segunda a sábado; demais dias sem atendimento |
| Ativado (ramo 29) | Clientes que compraram nos últimos 30 dias, do ramo de atividade 29, com uma única compra com o vendedor | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Preferência: segunda a sábado |
| Ativado (demais ramos) | Clientes que compraram nos últimos 30 dias, de ramo de atividade diferente de 29, com uma única compra com o vendedor | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Preferência: segunda a sábado |
| Ativo: compra regularmente | Clientes ativos para o vendedor, com frequência histórica de compra de menos de 14 dias, que não têm compra única com o vendedor | 10 dias | Preferência: segunda a sábado; demais dias sem atendimento |
| Estimular regularidade (ramo 29) | Clientes do ramo 29 que compraram com o vendedor nos últimos 59 dias, estão há pelo menos 21 dias sem comprar e não são de compra única | 30 dias | Não ativos, ou ativos com frequência histórica indefinida ou de pelo menos 14 dias. Preferência: segunda a sábado |
| Estimular regularidade (demais ramos) | Clientes de ramo diferente de 29 que compraram com o vendedor nos últimos 59 dias, estão há pelo menos 21 dias sem comprar e não são de compra única | 14 dias | Não ativos, ou ativos com frequência histórica indefinida ou de pelo menos 14 dias. Preferência: segunda a sábado |
| Em ruptura (ramo 29) | Clientes do ramo 29 que compraram com o vendedor nos últimos 89 dias, estão há mais de 59 dias sem comprar e não são de compra única | 14 dias | Não ativos, ou ativos com frequência histórica indefinida ou de pelo menos 14 dias. Preferência: segunda a sábado |
| Em ruptura (demais ramos) | Clientes de ramo diferente de 29 que compraram com o vendedor nos últimos 89 dias, estão há mais de 59 dias sem comprar e não são de compra única | 14 dias | Não ativos, ou ativos com frequência histórica indefinida ou de pelo menos 14 dias. Preferência: segunda a sábado |
| Resgate | Clientes sem comprar com o vendedor há mais de 90 dias e que não são de compra única | 10 dias | Não ativos, ou ativos com frequência histórica indefinida ou de pelo menos 14 dias. Preferência: segunda a sábado |

## Pontos de atenção

- A regra 'Freq. de 21d para Ativado: fez um pedido e ainda não comprou mais' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Freq. de 14d para Ativado: fez um pedido e ainda não comprou mais' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- As faixas misturam medidas de recência de compra de escopos diferentes (grupo de vendedores e próprio vendedor), então podem se sobrepor ou deixar lacunas.
- Clientes que nunca compraram com o vendedor, compraram nos últimos 20 dias ou compraram nos últimos 90 dias mas estão há mais de 89 dias sem comprar, e que não são de compra única, não se enquadram em nenhuma regra e ficam sem parametrização (se ativos, apenas os de frequência histórica indefinida ou de pelo menos 14 dias).
