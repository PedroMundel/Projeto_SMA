# regra_221.gobr

Regra de agendamento do time de televendas, com frequências de 7, 14, 21 e 28 dias conforme o histórico do cliente com o vendedor e o tempo desde a última compra. O atendimento tem preferência de segunda a sábado, e os demais dias ficam sem atendimento. Não há bloqueios de agenda, e a última regra nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Pré-qualificados | Clientes sem vendas para o vendedor | 21 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Clientes ativados | Clientes que estão há mais de 30 dias sem comprar, com alguma venda para o vendedor e uma única compra com ele | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Compra regular | Clientes que compraram nos últimos 30 dias, mas estão há mais de 21 dias sem comprar, e têm alguma venda para o vendedor | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Estimular regularidade | Clientes com venda para o vendedor que compraram nos últimos 21 dias ou, se não são de compra única, estão há mais de 60 dias sem comprar | 14 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Deixando de comprar | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com venda para o vendedor e sem ser de compra única | 7 dias | Preferência de segunda a sábado; demais dias sem atendimento |
| Resgate de clientes | Clientes que compraram nos últimos 90 dias ou estão há mais de 360 dias sem comprar [não traduzido: preferencia nos dias uteis e no sabado"] | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Resgate este cliente caso ele seja perfil' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Resgate este cliente caso ele seja perfil' tem um trecho não reconhecido, com possível erro de sintaxe: preferencia nos dias uteis e no sabado"
- Clientes do time televendas que nunca compraram e têm alguma venda (ativos ou inativos) para o vendedor não se enquadram em nenhuma regra e ficam sem parametrização.
