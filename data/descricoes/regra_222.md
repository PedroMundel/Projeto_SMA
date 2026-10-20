# regra_222.gobr

Regras de frequência para dois times. O time ruptura_global atende clientes adimplentes de grupos de ramos de atividade, conforme o tempo sem comprar. O time carteira organiza os clientes que compraram nos últimos 90 dias por curva A, B, C ou sem classificação, e trata à parte quem está sem comprar há mais de 90 dias. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ruptura: sem venda há mais de 30 dias | Clientes adimplentes que nunca compraram ou estão há mais de 30 dias sem comprar, dos ramos de atividade 10, 28, 32, 33, 37, 38 e mais 6 | 14 dias | Time ruptura_global |
| Ruptura: sem venda há mais de 45 dias | Clientes adimplentes que estão há mais de 45 dias sem comprar, dos ramos de atividade 1, 11, 12, 13, 14, 15 e mais 24 | 14 dias | Time ruptura_global |
| Curva A | Clientes que compraram nos últimos 90 dias e são curva A com a empresa | 14 dias | Time carteira |
| Curva B | Clientes que compraram nos últimos 90 dias e são curva B com a empresa | 21 dias | Time carteira |
| Curva C | Clientes que compraram nos últimos 90 dias e são curva C com a empresa | 28 dias | Time carteira |
| Sem classificação de curva | Clientes que compraram nos últimos 90 dias e não são curva A, B nem C com a empresa | 21 dias | Time carteira |
| Sem compra há mais de 90 dias | Clientes que nunca compraram ou estão há mais de 90 dias sem comprar | 21 dias | Time carteira |

## Pontos de atenção

- No time ruptura_global, várias combinações de clientes não se enquadram em nenhuma regra e ficam sem parametrização.
