# regra_155.gobr

Regra de agendamento do time de televendas por momento do relacionamento: prospects, leads recentes, primeira compra, clientes por curva A, B e C e estímulo de regularidade. Não são agendados pessoas físicas, filiais, clientes baixados na Receita Federal, inadimplentes e clientes com compra nos últimos 30 dias. As duas regras finais, de risco de inatividade e de risco de ativação por outro vendedor, nunca chegam a ser aplicadas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram nos últimos 30 dias | Não agendar |  |
| Ativação de novo cliente em potencial | Clientes que nunca compraram na empresa e estão cadastrados no ERP há pelo menos 30 dias | 7 dias |  |
| Requalificar lead | Clientes que nunca compraram na empresa e estão cadastrados no ERP há menos de 30 dias | 21 dias |  |
| Boas-vindas a novo cliente | Clientes que já compraram na empresa e têm uma única compra com o vendedor | 7 dias |  |
| Bom histórico de compra (curva A) | Clientes da curva A que compraram nos últimos 29 dias ou estão há mais de 45 dias sem comprar, sem ser de compra única com o vendedor | 14 dias |  |
| Bom histórico de compra (curva B) | Clientes da curva B que compraram nos últimos 29 dias ou estão há mais de 45 dias sem comprar, sem ser de compra única com o vendedor | 28 dias |  |
| Bom histórico de compra (curva C) | Clientes fora das curvas A e B que compraram nos últimos 29 dias ou estão há mais de 45 dias sem comprar, sem ser de compra única com o vendedor | 45 dias |  |
| Estimular regularidade de compra | Clientes que compraram nos últimos 45 dias, mas estão há pelo menos 30 dias sem comprar, sem ser de compra única com o vendedor | 28 dias |  |
| Risco de ficar inativo | Clientes que compraram nos últimos 60 dias ou estão há mais de 90 dias sem comprar | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Risco de ativação por outro RCA | Clientes de todo o time televendas, sem filtro | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Risco de ficar inativo' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Risco de ativação por outro RCA' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- O nome da regra 'Risco de ativação por outro RCA' fala em 90 dias, mas a regra usa outro valor.
- A cascata mistura medidas de recência de compra de escopos diferentes (empresa toda nas curvas A, B e C; grupo de vendedores no bloqueio de compra em 30 dias), então as faixas não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
