# regra_186.gobr

Regra de agendamento do time televendas. Primeiro deixam de ser agendados os clientes que compraram com o próprio vendedor nos últimos 7 dias e os que têm rota nos próximos 7 dias. Depois vêm as faixas por tempo sem comprar (nunca compraram, 180 a 360 dias, compra entre 7 e 60 dias com rota e visita, até 90 e até 180 dias), e a regra final atende todos os demais clientes.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra recente com o vendedor | Clientes que compraram com o próprio vendedor nos últimos 7 dias | Não agendar |  |
| Bloqueio: rota nos próximos dias | Clientes com data de rota futura nos próximos 7 dias | Não agendar |  |
| Nunca tirou pedido | Clientes sem vendas para a empresa | 14 dias |  |
| Ativar cliente | Clientes que compraram nos últimos 360 dias, mas estão há pelo menos 180 dias sem comprar, com compra no ano anterior e alguma venda para a empresa | 14 dias |  |
| Restabelecer relacionamento | Clientes que compraram com qualquer vendedor da empresa nos últimos 14 dias, com compra na empresa entre 181 e 360 dias atrás e sem compra entre 15 e 180 dias atrás | 14 dias | Com compra no ano anterior, exige: nunca comprou no grupo, comprou nele nos últimos 179 dias ou está há mais de 360 dias sem comprar. |
| Compra entre 7 e 30 dias, com rota e visita | Clientes com compra na empresa entre 7 e 30 dias atrás, com data de rota há 7 dias e visita na semana anterior, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Compra entre 31 e 60 dias, com rota e visita | Clientes com compra na empresa entre 31 e 60 dias atrás, com data de rota há 7 dias e visita na semana anterior, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Caminhando para inatividade | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Resgate de inativos | Clientes que compraram com qualquer vendedor da empresa nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Demais clientes | Todos os clientes do time televendas, exceto os já tratados pelas regras anteriores | 28 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- As faixas misturam medidas diferentes de última compra: na empresa toda ('Restabeleça relacionamento com este cliente que foi ativado!', 'Cliente caminhando para INATIVIDADE!...' e 'Resgaste este cliente!...'), no grupo de vendedores ('Ative este cliente!') e no próprio vendedor ('Não agendar clientes que compraram com o televendas em 7d.'). Por isso as faixas podem se sobrepor ou deixar lacunas.
