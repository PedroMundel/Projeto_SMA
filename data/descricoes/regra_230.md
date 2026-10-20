# regra_230.gobr

Regra de agendamento do time de televendas pelo histórico de compras com o próprio vendedor, em seis regras de frequência de 7, 14 e 21 dias: prospects, ativados, ativos, ativos a estimular, em ruptura e inativos. Antes delas, clientes inadimplentes não são agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospect | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativado | Clientes que já compraram com o próprio vendedor, mas só uma vez | 7 dias |  |
| Ativo: compra regularmente | Clientes ativos para o vendedor, com mais de uma compra com ele e frequência histórica de compra de menos de 16 dias | 14 dias |  |
| Ativo: estimular regularidade | Clientes com mais de uma compra com o próprio vendedor que compraram nos últimos 45 dias, mas estão há pelo menos 16 dias sem comprar | 14 dias |  |
| Em ruptura | Clientes com mais de uma compra com o próprio vendedor que compraram nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 7 dias |  |
| Inativo | Clientes com mais de uma compra com o próprio vendedor que estão há mais de 89 dias sem comprar com ele | 21 dias |  |

## Pontos de atenção

- Clientes com mais de uma compra com o próprio vendedor que compraram com ele nos últimos 15 dias, ou nos últimos 59 dias mas estão há mais de 45 dias sem comprar, não se enquadram em nenhuma regra e ficam sem parametrização (exceto os ativos com frequência histórica de compra de menos de 16 dias, tratados pela regra 'Ativo: compra regularmente').
