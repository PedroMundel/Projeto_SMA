# RegraInfinittoDesign.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro grupos: prospects, ativos, risco de inatividade e inativos. Antes dos grupos, deixam de ser agendados os clientes baixados na Receita Federal. Os inativos são a última faixa e recebem a frequência mais espaçada.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 14 dias |  |
| Risco de inatividade | Clientes que estão há mais de 60 dias sem comprar com qualquer vendedor da empresa e compraram no grupo de vendedores nos últimos 90 dias | 7 dias |  |
| Inativos | Clientes que estão há mais de 60 dias sem comprar na empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 28 dias |  |

## Pontos de atenção

- As faixas de tempo sem comprar misturam escopos diferentes (empresa toda e grupo de vendedores), por isso não se excluem automaticamente e podem se sobrepor ou deixar lacunas, como entre 'Ativo' e 'Risco de Inatividade'.
