# regra_171.gobr

Regra de agendamento do time de televendas por ciclo de vida do cliente: prospects, ativados, ativos de alta frequência e de compra regular, ativos a estimular, clientes em ruptura e inativos, com frequências de 7 a 21 dias. Antes das faixas, deixam de ser agendados os inadimplentes, os bloqueados, as filiais e os baixados na Receita Federal. A regra de inativos é a última, e parte dos clientes com compra entre 90 e 180 dias atrás não se enquadra em nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados para atendimento | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Ativados | Clientes que já compraram na empresa, cadastrados no ERP há pelo menos 30 dias e com uma única compra | 10 dias |  |
| Ativos de alta frequência | Clientes que compraram nos últimos 30 dias, com frequência histórica de compra de menos de 14 dias | 14 dias | Clientes de compra única entram só se cadastrados no ERP há menos de 30 dias |
| Ativos que compram regularmente | Clientes que compraram nos últimos 30 dias, com frequência histórica de compra entre 14 e 29 dias | Pelo histórico; sem histórico, entre 14 e 28 dias | Clientes de compra única entram só se cadastrados no ERP há menos de 30 dias |
| Ativos a estimular | Clientes que compraram nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Em ruptura | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias | Clientes de compra única entram só se cadastrados no ERP há menos de 30 dias |
| Inativos | Clientes que compraram nos últimos 89 dias ou estão há mais de 180 dias sem comprar, exceto os já tratados pelas regras anteriores | 21 dias |  |

## Pontos de atenção

- O nome da regra 'Freq. de 21d para Ativo: compra regularmente' fala em 21 dias, mas a regra usa outro valor: frequência calculada pelo histórico, entre 14 e 28 dias.
- Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar (com compra única, apenas os cadastrados no ERP há menos de 30 dias) não se enquadram em nenhuma regra e ficam sem parametrização.
