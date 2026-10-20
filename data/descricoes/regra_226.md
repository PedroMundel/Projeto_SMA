# regra_226.gobr

Regra de atendimento do time de televendas por situação de compra do cliente, em seis regras. Começa pelos clientes sem vendas para a empresa, passando por recém-ativados, regulares, compradores intercalados e inativos há mais de 120 e de 180 dias. Não há regras de bloqueio da agenda. A última regra, para clientes há mais de 180 dias sem comprar, nunca é aplicada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem vendas para a empresa | Clientes sem vendas para a empresa | 7 dias |  |
| Cliente ativado | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias, têm alguma venda para a empresa e uma única compra | 14 dias |  |
| Clientes regulares (mensais) | Clientes com frequência histórica de 30 dias, compraram nos últimos 120 dias e há mais de 30 dias sem comprar, ou nos últimos 30 dias com mais de uma compra | 28 dias |  |
| Compram mês sim, mês não | Clientes que compraram na empresa e com o próprio vendedor nos últimos 30 dias, há pelo menos 20 dias sem comprar, com frequência histórica diferente de 30 dias ou indefinida | Pelo histórico de compras, no máximo 60 dias | Sem histórico de compras, a frequência fica limitada a no máximo 60 dias |
| Sem comprar há mais de 120 dias | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e têm alguma venda para a empresa | 14 dias |  |
| Inativos há mais de 180 dias | Clientes que estão há mais de 180 dias sem comprar com qualquer vendedor da empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Resgate seu cliente inativo!' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores ('Ative essa oportunidade' e 'Mantenha seu cliente ativo!').
- As regras 'Cliente ativado!', 'Clientes regulares', 'Mantenha seu cliente ativo!' e 'Compram mês sim, mês não' misturam medidas de recência de compra de escopos diferentes (empresa e vendedor), então as faixas podem se sobrepor ou deixar lacunas.
- Clientes que nunca compraram ou que compraram nos últimos 120 dias, mas estão há mais de 30 dias sem comprar, com frequência histórica indefinida ou diferente de 30 dias, não se enquadram em nenhuma regra e ficam sem parametrização. O mesmo vale para clientes com compra nos últimos 30 dias que compraram com o próprio vendedor nos últimos 19 dias ou estão há mais de 30 dias sem comprar com ele.
