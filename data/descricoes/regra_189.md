# regra_189.gobr

Regra de agendamento do time de televendas organizada por ticket médio e ano da última compra. As três primeiras regras tratam a base de valor alto, a de valor médio e quem comprou só no ano anterior, com frequência semanal e dias de preferência. Em seguida vêm as regras de ativação e boas-vindas, de bom histórico de compra e de risco de inatividade. Não há bloqueios nem regra final.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Valor alto | Clientes sem compra na empresa no ano atual e com ticket médio maior que R$ 4999 | 7 dias | Preferência na segunda e na sexta; demais dias sem atendimento; parametrização fixa |
| Valor médio | Clientes sem compra na empresa no ano atual e com ticket médio menor que R$ 4999 | 7 dias | Preferência na terça e na sexta; demais dias sem atendimento; parametrização fixa |
| Última compra no ano anterior | Clientes com compra na empresa no ano anterior e sem compra no ano atual, fora das faixas de ticket médio maior ou menor que R$ 4999 | 7 dias | Preferência na quarta e na quinta; demais dias sem atendimento |
| Novo cliente em potencial | Clientes sem vendas para o vendedor, com compra na empresa no ano atual ou sem compra nos dois anos, fora das regras anteriores | 7 dias |  |
| Novo cliente ativado | Clientes com alguma venda para o vendedor e uma única compra com ele, com compra no ano atual ou sem compra nos dois anos | 7 dias |  |
| Bom histórico de compra | Clientes com frequência histórica de compra de até 14 dias e mais de uma compra com o vendedor, com compra no ano atual ou sem compra nos dois anos | Pelo histórico, entre 4 e 6 dias |  |
| Risco de inatividade | Clientes com compra com o vendedor nos últimos 24 dias ou há mais de 30 dias sem comprar, frequência histórica indefinida ou acima de 14 dias, e mais de uma compra | 7 dias |  |

## Pontos de atenção

- Clientes que compraram com o vendedor nos últimos 30 dias, mas estão há pelo menos 25 dias sem comprar, com frequência histórica indefinida ou de mais de 14 dias e mais de uma compra, não se enquadram em nenhuma regra e ficam sem parametrização.
