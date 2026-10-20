# regra_155.gobr

Regra de agendamento do time de televendas, organizada por etapa do relacionamento: prospects, clientes com uma única compra, clientes de curva A, B e C e estímulo de regularidade de compra. Deixam de ser agendados pessoas físicas, filiais, clientes baixados na Receita Federal, inadimplentes e quem comprou nos últimos 30 dias. As duas últimas regras, de risco de inatividade, nunca são aplicadas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixadas na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram nos últimos 30 dias | Não agendar |  |
| Ativação de novo cliente em potencial | Clientes que nunca compraram na empresa e estão cadastrados no ERP há pelo menos 30 dias | 7 dias |  |
| Requalificar lead | Clientes que nunca compraram na empresa e não estão cadastrados no ERP há pelo menos 30 dias | 21 dias |  |
| Boas-vindas a novo cliente | Clientes que já compraram na empresa e têm uma única compra com o vendedor | 7 dias |  |
| Bom histórico - Curva A | Clientes da curva A, sem compra única com o vendedor, que compraram na empresa nos últimos 29 dias ou estão há mais de 45 dias sem comprar | 14 dias |  |
| Bom histórico - Curva B | Clientes da curva B, sem compra única com o vendedor, que compraram na empresa nos últimos 29 dias ou estão há mais de 45 dias sem comprar | 28 dias |  |
| Bom histórico - Curva C | Clientes fora das curvas A e B, sem compra única com o vendedor, que compraram na empresa nos últimos 29 dias ou estão há mais de 45 dias sem comprar | 45 dias |  |
| Estimular regularidade de compra | Clientes que compraram na empresa nos últimos 45 dias, mas estão há pelo menos 30 dias sem comprar, sem compra única com o vendedor | 28 dias |  |
| Risco de ficar inativo | Clientes que compraram na empresa nos últimos 60 dias ou estão há mais de 90 dias sem comprar na empresa | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Risco de ativação por outro RCA | Todos os clientes do time televendas, sem filtro | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Atenção!!! Cliente com RISCO de ficar inativo' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Atenção!!! Seu cliente corre RISCO de ativação por outro RCA' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- O nome da regra 'Atenção!!! Seu cliente corre RISCO de ativação por outro RCA' fala em 90 dias, mas esse valor não aparece na condição da regra: nome e código podem estar divergentes.
- As regras misturam medidas de recência de compra diferentes (da empresa nas curvas A, B e C; do grupo de vendedores no bloqueio de compra em 30 dias), então as faixas podem se sobrepor ou deixar lacunas.
