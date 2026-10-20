# regra_121.gobr

Regra de agendamento do time de televendas por ciclo de vida e tempo desde a última compra, em faixas de até 30, 60, 90 e 120 dias, mais reativados, clientes de compra única e uma regra final. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal e as filiais. A regra final atende, a cada 7 dias, quem nunca comprou ou está há mais de 120 dias sem comprar.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Reativados | Clientes no ciclo de vida reativado com a empresa | 3 dias |  |
| Compra única | Clientes com uma única compra na empresa, exceto os já tratados pelas regras anteriores | 3 dias |  |
| Ativos recorrentes (até 30 dias) | Clientes que compraram nos últimos 30 dias, exceto reativados e de compra única | Pelo histórico de compras | Sem histórico, frequência limitada a no mínimo 3 dias e no máximo 21 dias |
| Ativos (30 a 60 dias) | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, exceto reativados e de compra única | 14 dias |  |
| Ativos (60 a 90 dias) | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto reativados e de compra única | 21 dias |  |
| Ativos (90 a 120 dias) | Clientes que compraram nos últimos 120 dias, mas estão há mais de 90 dias sem comprar, exceto reativados e de compra única | 14 dias |  |
| Demais clientes | Clientes que nunca compraram ou estão há mais de 120 dias sem comprar, exceto reativados e de compra única | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |
