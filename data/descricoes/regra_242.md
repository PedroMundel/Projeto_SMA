# regra_242.gobr

Regra de planejamento do time de televendas pela frequência histórica de compra do cliente (até 30, de 31 a 60, de 61 a 90 e de 91 a 180 dias), combinada com o tempo sem comprar. São sete faixas, com frequências de 21 e 15 dias. Não há regras de bloqueio nem regra final para os demais clientes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Freq. histórica até 30 dias | Clientes que compraram nos últimos 30 dias, estão há pelo menos 20 dias sem comprar e têm frequência histórica de compra de até 30 dias | 21 dias |  |
| Freq. histórica 31 a 60 dias (29 dias sem comprar) | Clientes que compraram nos últimos 44 dias, estão há pelo menos 29 dias sem comprar e têm frequência histórica de compra entre 31 e 60 dias | 21 dias |  |
| Freq. histórica 31 a 60 dias (44 dias sem comprar) | Clientes que compraram nos últimos 60 dias, estão há mais de 44 dias sem comprar e têm frequência histórica de compra entre 31 e 60 dias | 21 dias |  |
| Freq. histórica 61 a 90 dias (60 dias sem comprar) | Clientes que compraram nos últimos 90 dias, estão há mais de 60 dias sem comprar e têm frequência histórica de compra entre 61 e 90 dias | 15 dias |  |
| Freq. histórica 61 a 90 dias (90 dias sem comprar) | Clientes que compraram nos últimos 180 dias, estão há mais de 90 dias sem comprar e têm frequência histórica de compra entre 61 e 90 dias | 21 dias |  |
| Freq. histórica 91 a 180 dias (44 dias sem comprar) | Clientes que compraram nos últimos 120 dias, estão há pelo menos 44 dias sem comprar e têm frequência histórica de compra entre 91 e 180 dias | 21 dias |  |
| Freq. histórica 91 a 180 dias (120 dias sem comprar) | Clientes que compraram nos últimos 180 dias, estão há mais de 120 dias sem comprar e têm frequência histórica de compra entre 91 e 180 dias | 15 dias |  |

## Pontos de atenção

- Várias combinações de clientes não se enquadram em nenhuma regra e ficam sem parametrização.
