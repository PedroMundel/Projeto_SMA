# regra_190.gobr

Regra de agendamento do time Televendas por ciclo de vida e curva de compra, sem bloqueios. Há faixas para prospects, clientes com uma única compra, clientes em ruptura e inativos, com frequências de 21, 10, 7 e 14 dias. Os clientes ativos das curvas A, B e C têm frequência calculada pelo histórico de compras quando houve compra no mês, ou fixa de 7, 14 e 21 dias quando não houve. A regra final cobre todos os clientes que sobraram, a cada 21 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospect: fazer o primeiro pedido | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Ativado: primeiro pedido | Clientes que já compraram na empresa, estão cadastrados no ERP há pelo menos 30 dias e têm uma única compra | 10 dias |  |
| Em ruptura: risco de inatividade | Clientes adimplentes que compraram nos últimos 90 dias, mas estão há pelo menos 61 dias sem comprar | 7 dias | Compra única só entra se cadastrada no ERP há menos de 30 dias |
| Inativos: resgate de clientes sem compra | Clientes adimplentes, inativos na empresa, que nunca compraram no grupo de vendedores, compraram nele nos últimos 60 dias ou estão há mais de 90 dias sem comprar nele | 14 dias | Compra única só entra se cadastrada no ERP há menos de 30 dias |
| Ativo curva A com compra no mês | Clientes da curva A com a empresa e com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, no máximo 30 dias |  |
| Ativo curva A sem compra no mês | Clientes da curva A com a empresa, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Ativo curva B com compra no mês | Clientes da curva B com a empresa e com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, no máximo 30 dias |  |
| Ativo curva B sem compra no mês | Clientes da curva B com a empresa, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Ativo curva C com compra no mês | Clientes com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, no máximo 30 dias |  |
| Ativo curva C sem compra no mês | Todos os clientes do time, exceto os já tratados pelas regras anteriores | 21 dias | Regra final: vale para quem sobrou das anteriores |

## Pontos de atenção

- A condição da regra 'Ativo curva A com compra no mês' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- A condição da regra 'Ativo curva A sem compra no mês' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- A condição da regra 'Ativo curva B com compra no mês' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- A condição da regra 'Ativo curva B sem compra no mês' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- A condição da regra 'Ativo curva C com compra no mês' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- A condição da regra 'Ativo curva C sem compra no mês' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
