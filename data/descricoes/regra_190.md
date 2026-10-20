# regra_190.gobr

Regra de frequência do time Televendas por situação do cliente: prospects, primeiro pedido, risco de inatividade, inativos e clientes ativos das curvas A, B e demais. Entre os ativos, quem tem compra no mês atual segue a frequência do histórico, limitada a no máximo 30 dias; quem não tem segue 7, 14 ou 21 dias conforme a curva. Não há bloqueios de agenda, e a última regra atende todos os que sobraram.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Ativado: primeiro pedido | Clientes cadastrados no ERP há pelo menos 30 dias, que já compraram com algum vendedor da empresa e têm uma única compra | 10 dias |  |
| Em ruptura: risco de inatividade | Clientes adimplentes que compraram nos últimos 90 dias, mas estão há pelo menos 61 dias sem comprar, com mais de uma compra ou cadastrados há menos de 30 dias | 7 dias |  |
| Inativos: resgate | Clientes adimplentes, inativos na empresa, que nunca compraram no grupo de vendedores, compraram nele nos últimos 60 dias ou estão há mais de 90 dias sem comprar nele | 14 dias | Já compraram com algum vendedor da empresa; compra única só entra se cadastrados no ERP há menos de 30 dias |
| Ativos curva A com compra no mês | Clientes da curva A com a empresa e com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, até 30 dias |  |
| Ativos curva A sem compra no mês | Clientes da curva A com a empresa, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Ativos curva B com compra no mês | Clientes da curva B com a empresa e com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, até 30 dias |  |
| Ativos curva B sem compra no mês | Clientes da curva B com a empresa, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Ativos curva C com compra no mês | Clientes com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, até 30 dias |  |
| Ativos curva C sem compra no mês | Todos os clientes do time, exceto os já tratados pelas regras anteriores | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A regra 'Curva A (com compra no mês)' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Curva A (sem compra no mês)' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Curva B (com compra no mês)' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Curva B (sem compra no mês)' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Curva C (com compra no mês)' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Curva C (sem compra no mês)' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
