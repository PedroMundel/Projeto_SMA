# regra_191.gobr

Regra de agendamento do time de televendas por tempo desde a última compra, em faixas de pós-venda, alta regularidade, estímulo de regularidade, risco de inatividade e inativos, mais os prospects. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal e os inadimplentes. A regra final de clientes inativos cobre quem já comprou na empresa e está parado no grupo de vendedores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Pós-venda | Clientes que compraram nos últimos 7 dias | 21 dias |  |
| Alta regularidade | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | Pelo histórico mais 3 dias, entre 14 e 30 dias | Sem histórico de compras, a frequência fica limitada a no mínimo 14 e no máximo 30 dias |
| Estimular regularidade | Clientes que compraram nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias |  |
| Risco de inatividade | Clientes que compraram nos últimos 60 dias, mas estão há mais de 45 dias sem comprar | 7 dias |  |
| Clientes inativos | Clientes que já compraram na empresa e nunca compraram no grupo de vendedores ou estão há mais de 60 dias sem comprar nele | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |
