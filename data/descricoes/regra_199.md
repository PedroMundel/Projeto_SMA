# regra_199.gobr

Regra de agendamento do time de televendas por perfil e tempo desde a última compra, em seis faixas: prospects, recém-ativados, ativos que compram regularmente, ativos a estimular, clientes em ruptura e inativos. Antes das faixas, deixam de ser agendados os clientes inadimplentes e os bloqueados para atendimento. As frequências vão de 21 a 90 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram com qualquer vendedor da empresa | 30 dias |  |
| Ativado: um pedido | Clientes que compraram nos últimos 40 dias e têm uma única compra na empresa | 30 dias |  |
| Ativo: compra regularmente | Clientes ativos para o vendedor com frequência histórica de compra de menos de 21 dias; os de compra única só se há mais de 40 dias sem comprar no grupo | 90 dias |  |
| Ativo: estimular regularidade | Clientes que compraram na empresa nos últimos 59 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados pelas regras anteriores | 30 dias |  |
| Em ruptura: risco de inatividade | Clientes há mais de 59 e até 89 dias sem comprar, não ativos para o vendedor ou ativos com frequência histórica indefinida ou de pelo menos 21 dias | 21 dias |  |
| Inativo: reativar | Clientes há mais de 90 dias sem comprar na empresa, não ativos para o vendedor ou ativos com frequência histórica indefinida ou de pelo menos 21 dias | 45 dias |  |

## Pontos de atenção

- A regra 'Ativo: estimular a regularidade de compra' tem condição fragmentada demais para resumir; vale a condição própria, exceto os clientes já tratados pelas regras anteriores.
- As faixas misturam recência de compra da empresa toda (estimular a regularidade, ruptura e inativo) e do grupo de vendedores (ativado: fez um pedido); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Várias combinações de clientes do time televendas não são cobertas por nenhuma regra e ficam sem parametrização.
