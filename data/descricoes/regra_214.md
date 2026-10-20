# regra_214.gobr

Regra de agendamento do time de televendas por tempo desde a última compra com o vendedor, com frequências de 10, 14, 21 e 30 dias, separando também o ramo de atividade 29 dos demais e usando a frequência histórica de compra. O atendimento tem preferência de segunda a sábado. Deixam de ser agendados os clientes inadimplentes. Duas das regras de clientes ativados nunca são aplicadas, e há clientes que não caem em nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Compra única com o vendedor | Clientes com uma única compra com o vendedor | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Ativado (ramo 29) | Clientes que compraram nos últimos 30 dias, do ramo de atividade 29, com uma única compra com o vendedor | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Preferência de segunda a sábado. |
| Ativado (demais ramos) | Clientes que compraram nos últimos 30 dias, de ramo de atividade diferente de 29, com uma única compra com o vendedor | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Preferência de segunda a sábado. |
| Ativo: compra regularmente | Clientes ativos para o vendedor, com frequência histórica de compra de menos de 14 dias, que não são de compra única com o vendedor | 10 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Estimular regularidade (ramo 29) | Clientes do ramo de atividade 29 que não são de compra única, compraram com o vendedor nos últimos 59 dias e estão há pelo menos 21 dias sem comprar | 30 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Estimular regularidade (demais ramos) | Clientes de ramo de atividade diferente de 29 que não são de compra única, compraram com o vendedor nos últimos 59 dias e estão há pelo menos 21 dias sem comprar | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Em ruptura (ramo 29) | Clientes do ramo de atividade 29 que não são de compra única, compraram com o vendedor nos últimos 89 dias e estão há mais de 59 dias sem comprar | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Em ruptura (demais ramos) | Clientes de ramo de atividade diferente de 29 que não são de compra única, compraram com o vendedor nos últimos 89 dias e estão há mais de 59 dias sem comprar | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Resgate de cliente sem compra | Clientes que não são de compra única e estão há mais de 90 dias sem comprar com o vendedor | 10 dias | Preferência de segunda a sábado; demais dias sem atendimento |

## Pontos de atenção

- A regra 'Freq. de 21d para Ativado: fez um pedido e ainda não comprou mais' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Freq. de 14d para Ativado: fez um pedido e ainda não comprou mais' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- As faixas misturam medidas de recência de compra diferentes (no grupo de vendedores e com o próprio vendedor), que não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes que não são de compra única com o vendedor e que nunca compraram com ele, compraram com ele nos últimos 20 dias ou compraram nos últimos 90 dias mas estão há mais de 89 dias sem comprar não se enquadram em nenhuma regra e ficam sem parametrização, sendo não ativos para o vendedor ou, se ativos, com frequência histórica indefinida ou de pelo menos 14 dias.
