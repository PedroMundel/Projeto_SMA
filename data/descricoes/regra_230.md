# regra_230.gobr

Regra de agendamento do time televendas por ciclo de vida do cliente com o próprio vendedor: prospects, ativados, ativos regulares, ativos a estimular, em ruptura e inativos. Antes das faixas, deixam de ser agendados os clientes inadimplentes. A última faixa cobre os clientes sem comprar com o vendedor há mais de 89 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram com o próprio vendedor | 14 dias |  |
| Ativado: um pedido | Clientes que já compraram com o próprio vendedor, mas só uma vez | 7 dias |  |
| Ativo: compra regularmente | Clientes ativos para o vendedor, com mais de uma compra com ele e frequência histórica de compra de menos de 16 dias | 14 dias |  |
| Ativo: estimular regularidade | Clientes com mais de uma compra com o vendedor que compraram com ele nos últimos 45 dias e estão há pelo menos 16 dias sem comprar, exceto ativos com frequência histórica de menos de 16 dias | 14 dias |  |
| Em ruptura: risco de inatividade | Clientes com mais de uma compra com o vendedor que compraram com ele nos últimos 89 dias e estão há pelo menos 60 dias sem comprar, exceto ativos com frequência histórica de menos de 16 dias | 7 dias |  |
| Inativo: reativar | Clientes com mais de uma compra com o vendedor que estão há mais de 89 dias sem comprar com ele, exceto ativos com frequência histórica de menos de 16 dias | 21 dias |  |

## Pontos de atenção

- Clientes com mais de uma compra com o vendedor que compraram com ele nos últimos 15 dias, ou nos últimos 59 dias mas estão há mais de 45 dias sem comprar, exceto ativos com frequência histórica de menos de 16 dias, não se enquadram em nenhuma regra e ficam sem parametrização.
