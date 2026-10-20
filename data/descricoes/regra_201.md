# regra_201.gobr

Regra de agendamento do time de televendas, com frequências de 7 a 30 dias por perfil do cliente: prospects, inativos, ativados com uma única compra, ativos pela frequência histórica de compra e clientes em ruptura. Antes das faixas, deixam de ser agendados os clientes baixados na Receita Federal, os inadimplentes, os bloqueados e as filiais. A regra final também não agenda quem comprou recentemente mas não se enquadrou nas faixas anteriores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Prospect | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Inativo | Clientes que já compraram com o próprio vendedor, mas estão há mais de 90 dias sem comprar no grupo de vendedores | 28 dias |  |
| Ativado: um pedido só | Clientes que compraram no grupo de vendedores nos últimos 90 dias, cadastrados no ERP há pelo menos 60 dias e com uma única compra com o próprio vendedor | 30 dias |  |
| Ativo: alta frequência | Clientes que já compraram com o próprio vendedor e compraram no grupo de vendedores nos últimos 30 dias, com frequência histórica de compra de menos de 30 dias | 30 dias | Compra única só entra se cadastrada no ERP há menos de 60 dias |
| Ativo: compra regularmente | Clientes que já compraram com o próprio vendedor e compraram no grupo de vendedores nos últimos 30 dias, com frequência histórica de compra entre 30 e 89 dias | 30 dias | Compra única só entra se cadastrada no ERP há menos de 60 dias |
| Ativo: estimular regularidade | Clientes que compraram nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar, exceto os já tratados pelas regras anteriores | 10 dias |  |
| Em ruptura: risco de inatividade | Clientes que já compraram com o próprio vendedor e compraram no grupo de vendedores nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 14 dias | Compra única só entra se cadastrada no ERP há menos de 60 dias |
| Bloqueio: fora das regras padrão | Clientes que já compraram com o próprio vendedor e compraram no grupo de vendedores nos últimos 29 dias, com frequência histórica indefinida ou de pelo menos 90 dias | Não agendar | Regra final: vale para quem sobrou das anteriores. Compra única só entra se cadastrada há menos de 60 dias |

## Pontos de atenção

- A condição da regra 'Ativo: estimular regularidade' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
