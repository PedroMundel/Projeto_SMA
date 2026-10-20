# regra_139.gobr

Regra de agendamento de dois times de televendas: um de ativação de novos, que segue o histórico de compra do cliente em três faixas, e um de venda na base, que segue o tempo sem comprar com o próprio vendedor. Não são agendados os prospects do time de venda na base, os inadimplentes e os bloqueados para atendimento, nos dois times. Há combinações de clientes do time de venda na base que não caem em nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: prospects | Clientes que nunca compraram com qualquer vendedor da empresa | Não agendar | Vale só para o time farm_venda na base |
| Bloqueio: inadimplentes | Clientes inadimplentes dos dois times | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento, dos dois times | Não agendar |  |
| Padrão de compra em até 30 dias | Clientes com frequência histórica de compra de até 30 dias | Pelo histórico, até 30 dias | Time hunter_ativacao de novos; frequência limitada a no máximo 30 dias |
| Padrão de compra entre 30 e 90 dias | Clientes com frequência histórica de compra entre 31 e 90 dias | 21 dias | Time hunter_ativacao de novos |
| Padrão de compra acima de 90 dias | Clientes com frequência histórica de compra indefinida ou de mais de 90 dias | 30 dias | Time hunter_ativacao de novos |
| Estimular regularidade de compra | Clientes que compraram com o próprio vendedor nos últimos 90 dias, mas estão há pelo menos 45 dias sem comprar | 30 dias | Time farm_venda na base |
| Risco de inatividade | Clientes que compraram com o próprio vendedor nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 25 dias | Time farm_venda na base |
| Resgate de inativos | Clientes inativos para o vendedor que compraram com ele nos últimos 44 dias ou estão há mais de 180 dias sem comprar com ele | 21 dias | Time farm_venda na base |
| Alta frequência de compra | Clientes não inativos, com histórico de menos de 45 dias, que nunca compraram com o vendedor, compraram há até 44 dias ou estão há mais de 180 dias sem comprar | Pelo histórico, entre 40 e 45 dias | Time farm_venda na base; frequência limitada a no mínimo 40 dias e no máximo 45 dias |

## Pontos de atenção

- Clientes do time farm_venda na base não inativos para o vendedor, com frequência histórica indefinida ou de pelo menos 45 dias, que nunca compraram com o próprio vendedor, compraram nos últimos 44 dias ou estão há mais de 180 dias sem comprar, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes dos times hunter_ativacao de novos e farm_venda na base nessa mesma situação (não inativos, com frequência histórica indefinida ou de pelo menos 45 dias e esses mesmos tempos sem comprar com o próprio vendedor) não se enquadram em nenhuma regra e ficam sem parametrização.
