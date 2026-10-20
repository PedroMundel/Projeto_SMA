# regra_194.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em quatro faixas: prospects, ativos, risco de inatividade e inativos. Antes delas, deixam de ser agendados os clientes baixados na Receita Federal. A última faixa atende os inativos há mais de 90 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects | Clientes que nunca compraram na empresa | 7 dias |  |
| Ativos | Clientes que compraram na empresa nos últimos 60 dias | 14 dias |  |
| Risco de inatividade | Clientes que estão há mais de 60 dias sem comprar na empresa, mas compraram no grupo de vendedores nos últimos 90 dias | 7 dias |  |
| Inativos | Clientes que estão há mais de 60 dias sem comprar na empresa e nunca compraram no grupo de vendedores ou estão há mais de 90 dias sem comprar nele | 28 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- As faixas misturam escopos de recência de compra (empresa toda em 'Ativo (Com último pedido em até 60d atrás)' e grupo de vendedores em 'Risco de Inatividade (Com pedido entre 60 e 90d atrás)'), então podem se sobrepor ou deixar lacunas.
