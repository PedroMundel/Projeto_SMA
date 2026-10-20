# regra_171.gobr

Regra de agendamento do time de televendas por ciclo de vida do cliente, com frequências de 7 a 21 dias. Primeiro vêm os prospects e os clientes de primeira compra; depois, os ativos de alta frequência e de compra regular, os que precisam de estímulo, os em ruptura e os inativos. Deixam de ser agendados os inadimplentes, os bloqueados, as filiais e os baixados na Receita Federal.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram na empresa | 14 dias |  |
| Ativado: um pedido | Clientes que já compraram na empresa, cadastrados no ERP há pelo menos 30 dias e com uma única compra | 10 dias |  |
| Ativo: alta frequência de compra | Clientes que compraram nos últimos 30 dias e têm frequência histórica de compra de menos de 14 dias, incluindo os cadastrados no ERP há menos de 30 dias com uma única compra | 14 dias |  |
| Ativo: compra regularmente | Clientes que compraram nos últimos 30 dias e têm frequência histórica de compra entre 14 e 29 dias, incluindo os cadastrados no ERP há menos de 30 dias com uma única compra | Pelo histórico, entre 14 e 28 dias |  |
| Ativo: estimular a regularidade | Clientes que compraram nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Em ruptura: risco de ficar inativo | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, incluindo os cadastrados no ERP há menos de 30 dias com uma única compra | 7 dias |  |
| Inativo: reativar cliente sem compra | Clientes que compraram nos últimos 89 dias ou estão há mais de 180 dias sem comprar, exceto os já tratados pelas regras anteriores | 21 dias |  |

## Pontos de atenção

- O nome da regra 'Ativo: compra regularmente' (21d) fala em 21 dias, mas a regra usa outro valor.
- Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, e têm mais de uma compra ou foram cadastrados no ERP há menos de 30 dias com uma única compra, não se enquadram em nenhuma regra e ficam sem parametrização.
