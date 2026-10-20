# regra_228.gobr

Regra de agendamento do time de televendas, organizada pela relação do cliente com o próprio vendedor e pelo tempo sem comprar no grupo de vendedores. São seis faixas: clientes que nunca compraram com o vendedor, clientes de compra única, clientes que compram com regularidade (separados por curva C e demais curvas), clientes caminhando para inatividade e clientes inativos há mais de 180 dias. Não há regras de não agendar; a última faixa resgata os inativos.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos clientes | Clientes que nunca compraram com o próprio vendedor | 28 dias |  |
| Clientes ativados | Clientes que já compraram com o próprio vendedor, mas com uma única compra | 21 dias |  |
| Compra com regularidade (Curva C) | Clientes da curva C que compraram no grupo de vendedores nos últimos 90 dias, com mais de uma compra com o próprio vendedor | 7 dias |  |
| Compra com regularidade (Curva A e B) | Clientes fora da curva C que compraram no grupo de vendedores nos últimos 90 dias, com mais de uma compra com o próprio vendedor | 14 dias |  |
| Caminhando para inatividade | Clientes que compraram no grupo de vendedores nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, com mais de uma compra com o próprio vendedor | 28 dias |  |
| Clientes inativos | Clientes que estão há mais de 180 dias sem comprar no grupo de vendedores, com mais de uma compra com o próprio vendedor | 45 dias | Regra final: resgate dos inativos que sobraram das faixas anteriores |
