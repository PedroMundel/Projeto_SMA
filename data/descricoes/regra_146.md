# regra_146.gobr

Agendamento do time televendas por ramo de atividade e por situação de compra do cliente. Os ramos 15, 37 e 43 e os ramos 25, 4 e 41 com frequência histórica de compra de 7 dias são atendidos a cada 7 dias; cliente potencial e ativado seguem 30 dias, ativo que compra regularmente e em ruptura 21 dias, e inativo 45 dias. Inadimplentes não são agendados, e alguns clientes ficam sem nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Segmento Saude | Clientes dos ramos de atividade 15, 37 e 43 | 7 dias |  |
| Segmento FOOD | Clientes dos ramos de atividade 25, 4 e 41 com frequência histórica de compra de 7 dias | 7 dias |  |
| Cliente potencial | Clientes sem vendas para o vendedor fora dos ramos 15, 25, 37, 4, 41 e 43, e os dos ramos 25, 4 e 41 sem frequência histórica de 7 dias | 30 dias | Ramos 25, 4 e 41: frequência histórica indefinida, menor que 7 dias, ou maior que 7 dias sem vendas |
| Ativado: um único pedido | Clientes que compraram nos últimos 30 dias, com uma única compra com o vendedor, fora dos ramos 15, 25, 37, 4, 41 e 43 | 30 dias | Inclui ramos 25, 4 e 41 com frequência histórica indefinida, menor que 7 dias ou maior que 7 dias |
| Ativo: compra regularmente | Clientes com frequência histórica de compra de menos de 21 dias, exceto os já tratados pelas regras anteriores | 21 dias |  |
| Em ruptura | Clientes que compraram com o vendedor nos últimos 45 dias, mas há pelo menos 30 dias sem comprar, fora dos ramos 15, 37 e 43 | 21 dias | Frequência histórica indefinida ou de pelo menos 21 dias; compra única exige grupo há mais de 30 dias sem comprar |
| Inativo: reativar | Clientes sem comprar com o próprio vendedor há mais de 46 dias, fora dos ramos 15, 37 e 43 | 45 dias | Frequência histórica indefinida ou de pelo menos 21 dias; compra única exige grupo há mais de 30 dias sem comprar |

## Pontos de atenção

- A regra 'Ativo: compra regularmente' tem condição fragmentada demais para resumir; ela é descrita como frequência histórica de compra de menos de 21 dias, exceto os clientes já tratados pelas regras anteriores.
- As faixas misturam recência de compra do grupo de vendedores ('Ativado: Fez um pedido e ainda não comprou mais') e do próprio vendedor ('Em ruptura: risco de ficar inativo' e 'Inativo: reativar cliente sem compra'), então podem se sobrepor ou deixar clientes sem cobertura.
- Clientes de ramos fora de 15, 37 e 43, com frequência histórica indefinida ou de pelo menos 21 dias e alguma venda para o vendedor, que nunca compraram com o vendedor, compraram com ele nos últimos 29 dias ou nos últimos 46 dias mas estão há mais de 45 dias sem comprar, não se enquadram em nenhuma regra e ficam sem parametrização; no caso de compra única com o vendedor, isso vale quando o grupo de vendedores nunca comprou ou está há mais de 30 dias sem comprar.
