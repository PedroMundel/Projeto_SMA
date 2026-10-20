# regra_201.gobr

Regra de agendamento do time de televendas por tempo desde a última compra e frequência de compra, em oito faixas, sem carteiras. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal, os inadimplentes, os bloqueados e as filiais. Os prospects e os inativos vêm primeiro, seguidos dos ativados e dos ativos. Quem não se enquadra em nenhuma faixa também não é agendado.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Prospects | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Inativos | Clientes que já compraram com o próprio vendedor e estão há mais de 90 dias sem comprar no grupo de vendedores | 28 dias |  |
| Ativado: um pedido | Clientes que compraram no grupo de vendedores nos últimos 90 dias, cadastrados no ERP há pelo menos 60 dias e com uma única compra com o vendedor | 30 dias |  |
| Ativo: alta frequência | Clientes que compraram no grupo de vendedores nos últimos 30 dias, já compraram com o próprio vendedor e têm frequência histórica de compra de menos de 30 dias | 30 dias | Compra única só entra se cadastrado no ERP há menos de 60 dias |
| Ativo: compra regularmente | Clientes que compraram no grupo de vendedores nos últimos 30 dias, já compraram com o próprio vendedor e têm frequência histórica de compra entre 30 e 89 dias | 30 dias | Compra única só entra se cadastrado no ERP há menos de 60 dias |
| Ativo: estimular regularidade | Clientes que compraram nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar, exceto os já tratados pelas regras anteriores | 10 dias |  |
| Em ruptura: risco de inatividade | Clientes que já compraram com o próprio vendedor, compraram no grupo de vendedores nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Compra única só entra se cadastrado no ERP há menos de 60 dias |
| Demais clientes | Clientes que compraram no grupo de vendedores nos últimos 29 dias, já compraram com o próprio vendedor e têm frequência histórica indefinida ou de pelo menos 90 dias | Não agendar | Regra final; compra única só entra se cadastrado no ERP há menos de 60 dias |

## Pontos de atenção

- A regra 'Ativo: Estimular a regularidade de compra' tem condição fragmentada demais para resumir: vale para quem comprou nos últimos 60 dias, mas está há pelo menos 30 dias sem comprar, exceto os clientes já tratados pelas regras anteriores.
