# regra_208.gobr

Regra de agendamento do time de televendas por relacionamento com o vendedor e tempo desde a última compra no grupo de vendedores, com faixas de 7, 14 e 3 dias. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal, os inadimplentes, os bloqueados para atendimento e as filiais. Quem não se enquadra em nenhuma faixa também não é agendado.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativação de novos | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Relacionamento | Clientes que já compraram com o próprio vendedor, mas apenas uma vez | 14 dias |  |
| Comprou no mês | Clientes com compra no mês atual, frequência histórica de compra entre 90 e 120 dias e mais de uma compra com o próprio vendedor | 14 dias |  |
| Regularidade de compra | Clientes que compraram no grupo de vendedores nos últimos 30 dias e já compraram com o próprio vendedor mais de uma vez, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Risco de inatividade | Clientes que compraram no grupo de vendedores nos últimos 89 dias, estão há mais de 30 dias sem comprar e têm mais de uma compra com o próprio vendedor | 7 dias | Não inclui os já tratados pelas regras anteriores |
| Inativos | Clientes que compraram no grupo de vendedores nos últimos 120 dias, estão há mais de 89 dias sem comprar e têm mais de uma compra com o próprio vendedor | 3 dias | Não inclui os já tratados pelas regras anteriores |
| Demais clientes | Clientes sem comprar no grupo de vendedores há mais de 120 dias e com mais de uma compra com o próprio vendedor | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |
