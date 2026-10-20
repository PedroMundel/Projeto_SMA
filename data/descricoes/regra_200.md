# regra_200.gobr

Regra de agendamento do time de televendas, exceto o vendedor de id 1, por perfil e tempo desde a última compra, em sete regras: prospects, primeiro pedido, alta frequência, compra regular, estímulo, risco de inatividade e resgate de inativos. Não há regras de bloqueio. A última regra atende os inativos com mais de uma compra, com frequência de 21 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospect: primeiro pedido | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Ativado: primeiro pedido | Clientes que já compraram na empresa e têm uma única compra | 10 dias |  |
| Alta frequência de compra | Clientes que compraram nos últimos 30 dias e têm mais de uma compra na empresa | Pelo histórico, mais 5 dias | Histórico de compras mais 5 dias; sem histórico, limitada a no máximo 30 dias |
| Compra regularmente | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Estimular regularidade | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com mais de uma compra na empresa | 7 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra na empresa | 7 dias |  |
| Resgate de inativos | Clientes com mais de uma compra na empresa que nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 21 dias | Regra final: vale para quem sobrou das regras anteriores |

## Pontos de atenção

- A regra 'Compra regularmente' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- As faixas de recência misturam escopos diferentes (grupo de vendedores e vendedor) nas regras 'Alta frequência de compra', 'Estimular regularidade de compra', 'Risco de inatividade' e 'Compra regularmente'; por isso podem se sobrepor ou deixar lacunas.
