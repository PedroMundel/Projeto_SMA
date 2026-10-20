# regra_189.gobr

Regra de agendamento do time de televendas, organizada por compra no ano e ticket médio. As três primeiras faixas atendem semanalmente, em dias de preferência: base de valor alto, base de valor médio e quem teve a última compra no ano anterior. Os demais clientes são separados em ativação de novo cliente, boas-vindas, bom histórico de compra e risco de inatividade. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Base de valor alto | Clientes sem compra com a empresa no ano atual e com ticket médio maior que R$ 4999 | 7 dias | Preferência segunda e sexta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Base de valor médio | Clientes sem compra com a empresa no ano atual e com ticket médio menor que R$ 4999 | 7 dias | Preferência terça e sexta; demais dias sem atendimento. Parametrização fixa de frequência e dias |
| Última compra no ano anterior | Clientes com compra no ano anterior, sem compra no ano atual e com ticket médio nem maior nem menor que R$ 4999 | 7 dias | Preferência quarta e quinta; demais dias sem atendimento |
| Ativação de novo cliente | Clientes sem vendas para o vendedor, com compra no ano atual ou sem compra nos anos anterior e atual e ticket médio nem acima nem abaixo de R$ 4999 | 7 dias |  |
| Boas-vindas a cliente ativado | Clientes com compra única com o vendedor, com compra no ano atual ou sem compra nos anos anterior e atual e ticket médio nem acima nem abaixo de R$ 4999 | 7 dias |  |
| Bom histórico de compra | Clientes com frequência histórica de compra de até 14 dias e mais de uma compra com o vendedor, nas mesmas condições de ano e ticket da regra anterior | Pelo histórico, entre 4 e 6 dias | Se não houver histórico, a frequência fica limitada a no mínimo 4 dias e no máximo 6 dias |
| Risco de ficar inativo | Clientes de frequência histórica indefinida ou acima de 14 dias, que compraram com o vendedor nos últimos 24 dias ou estão há mais de 30 dias sem comprar com ele | 7 dias | Mesmas condições de ano e ticket da regra anterior; exclui quem tem compra única com o vendedor |

## Pontos de atenção

- Clientes com compra no ano atual e frequência histórica indefinida ou acima de 14 dias, que nunca compraram com o vendedor ou compraram com ele nos últimos 30 dias mas estão há pelo menos 25 dias sem comprar, e não são de compra única, não se enquadram em nenhuma regra e ficam sem parametrização. O mesmo vale para clientes sem compra nos anos anterior e atual, com ticket médio nem acima nem abaixo de R$ 4999, nessas mesmas condições.
