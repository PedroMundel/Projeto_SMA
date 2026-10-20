# regra_190.gobr

Regra de agendamento do time Televendas por ciclo de vida do cliente, em dez regras: prospects, clientes recém-ativados, em ruptura, inativos e ativos separados por curva A, B e C e por compra no mês. Nenhuma regra bloqueia a agenda. As regras de ativos descrevem o critério próprio de cada curva, sem as exceções das regras anteriores, e a última vale para todos os que sobrarem.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Ativados: boas-vindas | Clientes que já compraram na empresa, cadastrados no ERP há pelo menos 30 dias e com uma única compra | 10 dias |  |
| Em ruptura | Clientes adimplentes que compraram nos últimos 90 dias, mas estão há pelo menos 61 dias sem comprar | 7 dias | Compra única só entra se o cliente estiver cadastrado no ERP há menos de 30 dias |
| Inativos: resgate | Clientes adimplentes, inativos na empresa, que nunca compraram no grupo de vendedores, compraram nele nos últimos 60 dias ou estão há mais de 90 dias sem comprar nele | 14 dias | Compra única só entra se o cliente estiver cadastrado no ERP há menos de 30 dias |
| Ativos curva A, com compra no mês | Clientes da curva A com a empresa e com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, no máximo 30 dias |  |
| Ativos curva A, sem compra no mês | Clientes da curva A com a empresa, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Ativos curva B, com compra no mês | Clientes da curva B com a empresa e com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, no máximo 30 dias |  |
| Ativos curva B, sem compra no mês | Clientes da curva B com a empresa, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Ativos curva C, com compra no mês | Clientes com compra no mês atual, exceto os já tratados pelas regras anteriores | Pelo histórico, no máximo 30 dias |  |
| Ativos curva C, sem compra no mês | Todos os clientes do time Televendas, exceto os já tratados pelas regras anteriores | 21 dias | Regra final: vale para quem sobrou das regras anteriores |

## Pontos de atenção

- A condição da regra 'Curva A (com compra no mês)' é fragmentada demais para resumir: foi descrita como o critério próprio exceto os clientes já tratados pelas regras anteriores.
- A condição da regra 'Curva A (sem compra no mês)' é fragmentada demais para resumir: foi descrita como o critério próprio exceto os clientes já tratados pelas regras anteriores.
- A condição da regra 'Curva B (com compra no mês)' é fragmentada demais para resumir: foi descrita como o critério próprio exceto os clientes já tratados pelas regras anteriores.
- A condição da regra 'Curva B (sem compra no mês)' é fragmentada demais para resumir: foi descrita como o critério próprio exceto os clientes já tratados pelas regras anteriores.
- A condição da regra 'Curva C (com compra no mês)' é fragmentada demais para resumir: foi descrita como o critério próprio exceto os clientes já tratados pelas regras anteriores.
- A condição da regra 'Curva C (sem compra no mês)' é fragmentada demais para resumir: foi descrita como o critério próprio exceto os clientes já tratados pelas regras anteriores.
