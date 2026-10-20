# regra_226.gobr

Regra de agendamento do time de televendas por tempo desde a última compra e pela frequência histórica de compra, com frequências de 7, 14 e 28 dias. Clientes sem vendas para a empresa têm prioridade semanal, e os que compraram há pouco, os regulares e os parados há mais de 120 dias têm faixas próprias. Não há regras de bloqueio, e a última faixa (mais de 180 dias sem comprar) nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem vendas para a empresa | Clientes sem vendas para a empresa | 7 dias |  |
| Clientes recém-ativados | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias e têm uma única compra na empresa | 14 dias |  |
| Clientes regulares (mensais) | Clientes de frequência histórica entre 30 e 30 dias: há mais de 30 dias sem comprar (compra nos últimos 120) ou com mais de uma compra nos últimos 30 dias | 28 dias |  |
| Compram mês sim, mês não | Clientes que compraram nos últimos 30 dias, mas estão há pelo menos 20 dias sem comprar com o próprio vendedor, com frequência histórica indefinida, menor ou maior que 30 dias | Pelo histórico de compras | Sem histórico, limitada a no máximo 60 dias |
| Sem comprar há mais de 120 dias | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e já têm alguma venda para a empresa | 14 dias |  |
| Sem comprar há mais de 180 dias | Clientes que estão há mais de 180 dias sem comprar com qualquer vendedor da empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Resgate seu cliente inativo' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores ('Ative essa oportunidade' e 'Mantenha seu cliente ativo').
- As regras misturam medidas de recência de compra diferentes (da empresa toda e do próprio vendedor), então as faixas podem se sobrepor ou deixar lacunas.
- Clientes que nunca compraram com qualquer vendedor da empresa, ou que compraram nos últimos 120 dias mas estão há mais de 30 dias sem comprar, com frequência histórica indefinida, menor ou maior que 30 dias, não se enquadram em nenhuma regra e ficam sem parametrização. O mesmo vale para quem nunca comprou e tem frequência histórica entre 30 e 30 dias, e para quem comprou nos últimos 30 dias com histórico indefinido ou diferente de 30 dias, mas nunca comprou com o próprio vendedor, comprou com ele há menos de 20 dias ou está há mais de 30 dias sem comprar com ele.
