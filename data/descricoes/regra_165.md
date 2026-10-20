# regra_165.gobr

Regra de agendamento do time televendas por tempo sem comprar e por frequência histórica de compra, usando segmentações da carteira fixa dos vendedores do time campo (1 a 7, 16 a 30, 31 a 45 e 61 a 90 dias). Quem está há mais de 90 dias sem comprar é agendado a cada 7 dias, e as demais faixas usam 14, 21 e 28 dias. Deixam de ser agendados os clientes inativos inadimplentes e, na regra final, os que não se enquadram em nenhuma regra padrão.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inativos inadimplentes | Clientes inativos e inadimplentes | Não agendar |  |
| Mais de 90 dias sem compra | Clientes que estão há mais de 90 dias sem comprar | 7 dias |  |
| Frequência histórica de 1 a 7 dias | Clientes que compraram nos últimos 7 dias ou compraram nos últimos 90 dias, mas estão há mais de 15 dias sem comprar | 14 dias |  |
| Frequência histórica de 16 a 30 dias | Clientes fora da segmentação freq_hist_1a7 que compraram nos últimos 30 dias, ou nos últimos 90 dias mas estão há mais de 45 dias sem comprar | 28 dias | Também clientes da freq_hist_1a7 que compraram nos últimos 15 dias, mas estão há mais de 7 dias sem comprar |
| Frequência histórica de 31 a 45 dias | Clientes fora das segmentações freq_hist_16a30 e freq_hist_1a7 que compraram nos últimos 45 dias, ou nos últimos 90 dias mas estão há mais de 60 dias sem comprar | 21 dias | Também freq_hist_16a30 (compra em 45 dias, mais de 30 sem comprar) e freq_hist_1a7 (compra em 15 dias, mais de 7 sem comprar) |
| Frequência histórica de 61 a 90 dias | Clientes que estão há mais de 90 dias sem comprar | 15 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Bloqueio: fora das regras padrão | Clientes de todo o time televendas, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A regra 'Clientes com frequência histórica de pedidos entre 61 e 90 dias, e sem compra há 90 dias.' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
