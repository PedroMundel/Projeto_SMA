# regra_199.gobr

Regra de agendamento do time de televendas por situação e tempo desde a última compra, em seis faixas: prospects, ativados, ativos que compram regularmente, ativos a estimular, em ruptura e inativos. Antes das faixas, deixam de ser agendados os clientes inadimplentes e os bloqueados para atendimento. A última faixa atende os inativos, com frequência de 45 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram com qualquer vendedor da empresa | 30 dias |  |
| Ativado: um pedido | Clientes que compraram nos últimos 40 dias e têm uma única compra na empresa | 30 dias |  |
| Ativo: compra regularmente | Clientes ativos para o vendedor com frequência histórica de compra de menos de 21 dias e mais de uma compra na empresa | 90 dias | Compra única entra só se nunca comprou no grupo ou está há mais de 40 dias sem comprar nele |
| Ativo: estimular regularidade | Clientes que compraram na empresa nos últimos 59 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados pelas regras anteriores | 30 dias |  |
| Em ruptura: risco de inatividade | Clientes que compraram na empresa nos últimos 89 dias, mas estão há mais de 59 dias sem comprar, não ativos para o vendedor | 21 dias | Também entram ativos para o vendedor com frequência histórica indefinida ou de pelo menos 21 dias |
| Inativo: reativar | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa, não ativos para o vendedor | 45 dias | Também entram ativos para o vendedor com frequência histórica indefinida ou de pelo menos 21 dias |

## Pontos de atenção

- A regra 'Ativo: estimular a regularidade de compra' tem condição fragmentada demais para resumir: vale para quem comprou nos últimos 59 dias e está há mais de 30 dias sem comprar, exceto os já tratados pelas regras anteriores.
- As faixas de recência misturam escopos diferentes (empresa toda e grupo de vendedores) nas regras 'Ativo: estimular a regularidade de compra', 'Em ruptura: risco de ficar inativo', 'Inativo: reativar cliente sem compra' e 'Ativado: fez um pedido e ainda não comprou mais'; por isso podem se sobrepor ou deixar lacunas.
- Várias combinações de clientes não se enquadram em nenhuma regra e ficam sem parametrização.
