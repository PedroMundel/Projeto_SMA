# regra_139.gobr

Regra de agendamento para dois times. O time hunter_ativacao de novos segue a frequência histórica de compra do cliente, em três faixas (até 30 dias, entre 31 e 90 dias e mais de 90 dias). O time farm_venda na base segue o tempo sem comprar com o próprio vendedor e a frequência histórica. Não são agendados os inadimplentes, os bloqueados para atendimento e, no time farm_venda na base, os prospects.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: prospects | Clientes que nunca compraram com qualquer vendedor da empresa | Não agendar | Vale só para o time farm_venda na base |
| Bloqueio: inadimplentes | Clientes inadimplentes dos times hunter_ativacao de novos e farm_venda na base | Não agendar |  |
| Bloqueio: bloqueados para atendimento | Clientes bloqueados para atendimento, dos times hunter_ativacao de novos e farm_venda na base | Não agendar |  |
| Padrão de compra em até 30 dias | Clientes com frequência histórica de compra de até 30 dias | Pelo histórico de compras | Time hunter_ativacao de novos. Sem histórico, limitada a no máximo 30 dias |
| Padrão de compra entre 30 e 90 dias | Clientes com frequência histórica de compra entre 31 e 90 dias | 21 dias | Time hunter_ativacao de novos |
| Padrão de compra maior que 90 dias | Clientes com frequência histórica indefinida ou de compra de mais de 90 dias, exceto os já tratados pelas regras anteriores | 30 dias | Time hunter_ativacao de novos |
| Estimular regularidade de compra | Clientes que compraram com o próprio vendedor nos últimos 90 dias, mas estão há pelo menos 45 dias sem comprar | 30 dias | Time farm_venda na base |
| Risco de inatividade | Clientes que compraram com o próprio vendedor nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 25 dias | Time farm_venda na base |
| Resgate de cliente sem compra - Inativos | Clientes inativos para o vendedor que nunca compraram com ele, compraram nos últimos 44 dias ou estão há mais de 180 dias sem comprar com ele | 21 dias | Time farm_venda na base |
| Alta frequência de compra | Clientes não inativos com frequência histórica de menos de 45 dias; nunca compraram com o vendedor, compraram nos últimos 44 dias ou estão há mais de 180 dias sem comprar | Pelo histórico de compras | Time farm_venda na base. Sem histórico, no mínimo 40 e no máximo 45 dias |

## Pontos de atenção

- Clientes do time farm_venda na base que nunca compraram com o próprio vendedor, compraram com ele nos últimos 44 dias ou estão há mais de 180 dias sem comprar com ele, têm frequência histórica indefinida ou de pelo menos 45 dias e não são inativos para o vendedor não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes dos times hunter_ativacao de novos e farm_venda na base que nunca compraram com o próprio vendedor, compraram com ele nos últimos 44 dias ou estão há mais de 180 dias sem comprar com ele, têm frequência histórica indefinida ou de pelo menos 45 dias e não são inativos para o vendedor não se enquadram em nenhuma regra e ficam sem parametrização.
