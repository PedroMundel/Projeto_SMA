# regra_215.gobr

Regra de agendamento do time de televendas com frequência única de 7 dias para todas as seis faixas, que se diferenciam pelo tempo desde a última compra com o vendedor: primeira compra, prospect ativado, compra regularmente, estimular regularidade, risco de inatividade e resgate. Não há bloqueios de agenda. Clientes de compra única entram nas faixas apenas se houve compra recente no grupo de vendedores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Primeira compra | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Prospect ativado | Clientes que já compraram com o próprio vendedor, com uma única compra com ele, e estão há mais de 20 dias sem comprar no grupo de vendedores | 7 dias |  |
| Compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Compra única só entra se houve compra no grupo de vendedores nos últimos 20 dias |
| Ativo: estimular regularidade | Clientes que compraram com o próprio vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Compra única só entra se houve compra no grupo de vendedores nos últimos 20 dias |
| Risco de inatividade | Clientes que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias | Compra única só entra se houve compra no grupo de vendedores nos últimos 20 dias |
| Resgate de cliente sem compra | Clientes que estão há mais de 90 dias sem comprar com o próprio vendedor | 7 dias | Compra única só entra se houve compra no grupo de vendedores nos últimos 20 dias |

## Pontos de atenção

- A cascata mistura medidas de recência de compra de escopos diferentes (grupo de vendedores em 'Prospect ativado' e vendedor em 'Compra regularmente', 'Ativo: estimular a regularidade de compra' e 'Risco de inatividade'); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
