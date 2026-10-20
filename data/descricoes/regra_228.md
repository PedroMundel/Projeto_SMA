# regra_228.gobr

Regra de atendimento do time de televendas, organizada pelo histórico de compra do cliente com o próprio vendedor e no grupo de vendedores. Há seis faixas: clientes que nunca compraram, de compra única, regulares das curvas C e A/B, em risco de inatividade e inativos, com frequências de 7 a 45 dias. Não há bloqueios de agenda, e a última faixa resgata quem está há mais de 180 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos clientes | Clientes que nunca compraram com o próprio vendedor | 28 dias |  |
| Clientes ativados | Clientes que já compraram com o próprio vendedor, mas apenas uma vez | 21 dias |  |
| Compra regular (Curva C) | Clientes curva C na empresa que compraram no grupo de vendedores nos últimos 90 dias e já compraram mais de uma vez com o próprio vendedor | 7 dias |  |
| Compra regular (Curva A e B) | Clientes fora da curva C na empresa que compraram no grupo de vendedores nos últimos 90 dias e já compraram mais de uma vez com o próprio vendedor | 14 dias |  |
| Caminhando para inatividade | Clientes que compraram no grupo de vendedores nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, e não são de compra única com o vendedor | 28 dias |  |
| Resgate de inativos | Clientes que estão há mais de 180 dias sem comprar no grupo de vendedores e não são de compra única com o vendedor | 45 dias | Última faixa: atende quem passou de 180 dias sem comprar |
