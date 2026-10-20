# regra_200.gobr

Regra de agendamento do time de televendas, exceto o vendedor de id 1, por situação e tempo desde a última compra: prospects, primeiro pedido, alta frequência de compra e faixas de até 30, 60 e 90 dias, mais o resgate de quem está há mais de 90 dias sem comprar no grupo. Não há bloqueios. A regra de compra regular nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Ativado: boas-vindas ao primeiro pedido | Clientes que já compraram na empresa e têm uma única compra | 10 dias |  |
| Alta frequência de compra | Clientes que compraram nos últimos 30 dias e têm mais de uma compra na empresa | Pelo histórico mais 5 dias, no máximo 30 dias |  |
| Compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 30 dias, exceto os já tratados pelas regras anteriores | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Estimular regularidade de compra | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com mais de uma compra na empresa | 7 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra na empresa | 7 dias |  |
| Resgate de inativos | Clientes com mais de uma compra na empresa que nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 21 dias |  |

## Pontos de atenção

- A regra 'Freq. de 14d para Compra regularmente' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A sequência de regras mistura medidas diferentes de tempo sem comprar (grupo e vendedor); faixas de medidas diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
