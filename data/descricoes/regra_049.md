# regra_049.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em três faixas (até 30 dias, até 45 dias e mais de 45 dias) mais os prospects. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal. Clientes que já compraram na empresa, mas nunca no grupo de vendedores, não entram em nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Clientes ativos | Clientes que compraram nos últimos 30 dias | 14 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias |  |
| Inativos | Clientes que estão há mais de 45 dias sem comprar | 14 dias |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |

## Pontos de atenção

- Clientes que já compraram com qualquer vendedor da empresa e nunca compraram no grupo de vendedores não se enquadram em nenhuma regra e ficam sem parametrização.
