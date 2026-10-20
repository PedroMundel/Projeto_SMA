# regra_108.gobr

Regra de agendamento do time de televendas, organizada por histórico de compra com o próprio vendedor, ramo de atividade 37 e frequência histórica de compra. Há faixas de 7 dias, 14 dias e 21 dias, com tratamento próprio para quem nunca comprou e para quem comprou uma única vez. Antes das faixas, deixam de ser agendados os clientes inadimplentes. A última regra atende os demais clientes que compraram nos últimos 90 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Nunca compraram com o vendedor | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Ramo 37 com compra única | Clientes do ramo de atividade 37 que já compraram com o próprio vendedor, em uma única compra | 21 dias |  |
| Compra única (outros ramos) | Clientes de ramo de atividade diferente de 37 que já compraram com o próprio vendedor, em uma única compra | 7 dias |  |
| Frequência histórica menor que 11 dias | Clientes que já compraram com o próprio vendedor, com frequência histórica de compra de menos de 11 dias, sem ser compra única | 7 dias |  |
| Ramo 37, compra recente ou antiga | Clientes do ramo de atividade 37 que compraram com o próprio vendedor nos últimos 59 dias ou estão há mais de 89 dias sem comprar | 14 dias | Exclui compra única; frequência histórica indefinida ou de pelo menos 11 dias. |
| Ramo 37, intermediários | Clientes do ramo de atividade 37 que compraram com o próprio vendedor nos últimos 89 dias, mas estão há mais de 59 dias sem comprar | 21 dias | Exclui compra única; frequência histórica indefinida ou de pelo menos 11 dias. |
| Inativos (outros ramos) | Clientes de ramo de atividade diferente de 37 que já compraram com o próprio vendedor e estão no ciclo de vida inativo com ele | 21 dias | Exclui compra única; frequência histórica indefinida ou de pelo menos 11 dias. |
| Fora do ciclo inativo (outros ramos) | Clientes de ramo de atividade diferente de 37, fora do ciclo de vida inativo, que estão há mais de 90 dias sem comprar com o próprio vendedor | 7 dias | Exclui compra única; frequência histórica indefinida ou de pelo menos 11 dias. |
| Demais clientes | Clientes de ramo de atividade diferente de 37, fora do ciclo de vida inativo, que compraram com o próprio vendedor nos últimos 90 dias | 7 dias | Exclui compra única; frequência histórica indefinida ou de pelo menos 11 dias. |

## Pontos de atenção

- O nome da regra 'Freq. de 21d para clientes que comprou ultima vez com o vendedor a mais de 90 dias' fala em 90 dias, mas a regra usa outro valor.
