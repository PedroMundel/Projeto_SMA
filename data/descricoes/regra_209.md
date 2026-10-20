# regra_209.gobr

Regra de agendamento do time de televendas com três frequências: 7 dias para clientes novos e para os que compram com regularidade, e 17 dias para os que precisam de acompanhamento. Deixam de ser agendados os inadimplentes, as filiais e os clientes sem comprar com o próprio vendedor há mais de 90 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: fora de recência (90 dias) | Clientes que estão há mais de 90 dias sem comprar com o próprio vendedor | Não agendar |  |
| Novos clientes | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Compra com regularidade | Clientes que compraram com o próprio vendedor nos últimos 30 dias e têm frequência histórica de compra de até 30 dias | 7 dias |  |
| Precisa de acompanhamento | Clientes que compraram com o próprio vendedor nos últimos 30 dias e têm frequência histórica indefinida ou de mais de 30 dias | 17 dias |  |

## Pontos de atenção

- Todos os clientes do time televendas ficam fora de qualquer regra e sem parametrização, segundo a análise do pacote.
