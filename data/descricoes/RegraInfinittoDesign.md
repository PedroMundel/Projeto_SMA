# RegraInfinittoDesign.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas: prospects, ativos (até 60 dias), risco de inatividade (entre 60 e 90 dias) e inativos (mais de 90 dias). Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal. A última faixa recolhe os clientes inativos que sobraram das anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram com nenhum vendedor da empresa | 7 dias |  |
| Ativos | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 14 dias |  |
| Risco de inatividade | Clientes que estão há mais de 60 dias sem comprar com qualquer vendedor da empresa, mas compraram no grupo de vendedores nos últimos 90 dias | 7 dias |  |
| Inativos | Clientes que estão há mais de 60 dias sem comprar com qualquer vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 28 dias |  |

## Pontos de atenção

- A cascata mistura medidas de tempo sem compra de escopos diferentes (empresa toda nas faixas 'Ativo' e geral, grupo de vendedores no 'Risco de Inatividade'); as faixas não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
