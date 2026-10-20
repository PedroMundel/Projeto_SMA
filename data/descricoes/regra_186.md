# regra_186.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em oito faixas de frequência (de 7, 14 e 28 dias), com a última delas atendendo quem sobrou. Não são agendados os clientes que compraram com o próprio vendedor nos últimos 7 dias nem os que têm rota nos próximos 7 dias. Clientes sem vendas para a empresa têm frequência de 14 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra recente com o vendedor | Clientes que compraram com o próprio vendedor nos últimos 7 dias | Não agendar |  |
| Bloqueio: rota nos próximos 7 dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Nunca tirou pedido | Clientes sem vendas para a empresa | 14 dias |  |
| Ative este cliente | Clientes que compraram nos últimos 360 dias, mas estão há pelo menos 180 dias sem comprar, com compra no ano anterior e alguma venda para a empresa | 14 dias |  |
| Restabelecer relacionamento | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias, com compra entre 181 e 360 dias atrás e sem compra entre 15 e 180 dias atrás | 14 dias | Há duas variantes, conforme a compra no ano anterior e as compras no grupo de vendedores |
| Regularidade de compra (pedido em 30d) | Clientes com compra na empresa entre 7 e 30 dias atrás, data de rota há 7 dias e visita na semana anterior, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Último pedido entre 30d e 60d | Clientes com compra na empresa entre 31 e 60 dias atrás, data de rota há 7 dias e visita na semana anterior, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Caminhando para inatividade | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Resgate (último pedido entre 90d e 180d) | Clientes que compraram com qualquer vendedor da empresa nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Demais clientes | Todos os clientes do time, exceto os já tratados pelas regras anteriores | 28 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A regra 'Mantenha a regularidade de compra...' tem condição fragmentada demais para resumir; o critério mostra a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Garanta regularidade de compra e relacionamento...' tem condição fragmentada demais para resumir; o critério mostra a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Cliente caminhando para INATIVIDADE!' tem condição fragmentada demais para resumir; o critério mostra a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Resgaste este cliente!' tem condição fragmentada demais para resumir; o critério mostra a condição própria, exceto os clientes já tratados pelas regras anteriores.
- A regra 'Atendimento ao cliente que não se enquadrou nas demais regras' tem condição fragmentada demais para resumir; o critério mostra a condição própria, exceto os clientes já tratados pelas regras anteriores.
- As faixas misturam escopos de recência de compra (global, grupo de vendedores e vendedor), então regras de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
