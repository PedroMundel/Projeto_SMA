# regra_230.gobr

Regra de agendamento do time de televendas por situação do cliente com o próprio vendedor. Inadimplentes não são agendados. As demais cinco faixas dividem os clientes em prospects, ativados com compra única, ativos regulares, ativos a estimular, em ruptura e inativos, com frequências de 7, 14 e 21 dias. A última regra reativa os clientes sem compra há mais de 89 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativado: um único pedido | Clientes que já compraram com o próprio vendedor, mas com uma única compra | 7 dias |  |
| Ativo: compra regularmente | Clientes com mais de uma compra com o próprio vendedor, ativos para o vendedor e com frequência histórica de compra de menos de 16 dias | 14 dias |  |
| Ativo: estimular regularidade | Clientes com mais de uma compra com o próprio vendedor, que compraram com ele nos últimos 45 dias, mas estão há pelo menos 16 dias sem comprar | 14 dias | Não inclui ativos com frequência histórica de menos de 16 dias, já tratados antes |
| Em ruptura | Clientes com mais de uma compra com o próprio vendedor, que compraram com ele nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 7 dias | Não inclui ativos com frequência histórica de menos de 16 dias, já tratados antes |
| Inativo: reativar | Clientes com mais de uma compra com o próprio vendedor, que estão há mais de 89 dias sem comprar com ele | 21 dias | Regra final. Não inclui ativos com frequência histórica de menos de 16 dias, já tratados antes |

## Pontos de atenção

- Clientes com mais de uma compra com o próprio vendedor que compraram nos últimos 15 dias, ou nos últimos 59 dias mas estão há mais de 45 dias sem comprar, não se enquadram em nenhuma regra e ficam sem parametrização, exceto os ativos com frequência histórica de menos de 16 dias.
