# regra_227.gobr

Regra de agendamento do time felipe, de televendas, que começa pela cobertura fixa de clientes com data de rota há 7 dias. Os demais seguem faixas por tempo sem comprar: prospects, compra entre 30 e 90 dias e sem compra há mais de 90 dias. Não são agendados os clientes com compra nos últimos 30 dias, e a regra final, que bloquearia os clientes não cobertos, nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Cobertura de rota | Clientes com data de rota há 7 dias | 1 dia | Parametrização fixa: frequência e dias são restrição rígida para o gerador de agendas |
| Bloqueio: compra em 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias, exceto os com data de rota há 7 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa, exceto os com data de rota há 7 dias | 60 dias |  |
| Compra entre 30 e 90 dias | Clientes que compraram nos últimos 90 dias, mas estão há mais de 30 dias sem comprar, exceto os com data de rota há 7 dias | 15 dias |  |
| Inativos há mais de 90 dias | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa, exceto os com data de rota há 7 dias | 10 dias |  |
| Bloqueio: clientes não cobertos | Todos os clientes do time, sem filtro | Não agendar | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- O bloqueio 'Não agendar clientes com compra em 30 dias' vem depois da regra de cobertura de rota, então não bloqueia clientes que já entraram nela.
- A regra 'Nao agendar clientes nao cobertos pelas regras' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
