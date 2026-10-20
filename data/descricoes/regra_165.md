# regra_165.gobr

Regra de agendamento do time televendas por tempo sem comprar e por faixas de frequência histórica de compra (1 a 7, 16 a 30, 31 a 45 e 61 a 90 dias), definidas sobre carteiras do time campo. Clientes inativos inadimplentes não são agendados. A regra final também não agenda quem não se enquadra em nenhuma das anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inativos inadimplentes | Clientes inativos com a empresa e inadimplentes | Não agendar |  |
| Mais de 90 dias sem compra | Clientes que estão há mais de 90 dias sem comprar | 7 dias |  |
| Frequência histórica de 1 a 7 dias | Clientes com frequência histórica de 1 a 7 dias que compraram nos últimos 7 dias, ou nos últimos 90 dias mas estão há mais de 15 dias sem comprar | 14 dias |  |
| Frequência histórica de 16 a 30 dias | Clientes de frequência histórica 16 a 30 dias (não 1 a 7) com compra nos últimos 30 dias, ou nos últimos 90 dias mas há mais de 45 dias sem comprar | 28 dias | Quem está também na faixa 1 a 7 entra se comprou nos últimos 15 dias e está há mais de 7 dias sem comprar |
| Frequência histórica de 31 a 45 dias | Clientes de frequência histórica 31 a 45 dias com compra nos últimos 45 dias, ou nos últimos 90 dias mas há mais de 60 dias sem comprar | 21 dias | Vale para quem está fora das faixas 1 a 7 e 16 a 30; nelas há variações com janelas de 15 e 45 dias |
| Frequência histórica de 61 a 90 dias | Clientes com frequência histórica de 61 a 90 dias que estão há mais de 90 dias sem comprar | 15 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Demais clientes | Todos os clientes do time, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das anteriores |

## Pontos de atenção

- A regra 'Clientes com frequência histórica de pedidos entre 61 e 90 dias' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A condição da regra 'Não agendar clientes que não se enquadrem em nenhuma regra padrão' é complexa demais para resumir; ela foi descrita como todos os clientes, exceto os já tratados pelas regras anteriores.
