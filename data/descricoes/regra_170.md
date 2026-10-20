# regra_170.gobr

Regra de agendamento para todos os vendedores, organizada pelo ramo de atividade do cliente, por ele ser ativo ou não para o vendedor e pelo tempo sem comprar. Dois bloqueios impedem o agendamento: distribuidores ativos com vendas no grupo em 60 dias e demais ativos com vendas no grupo em 30 dias. As faixas de frequência são de 15, 21 e 30 dias, e a última regra trata os clientes não ativos e os prospects.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Distribuidor sem vendas em 60 dias | Clientes ativos para o vendedor, do ramo DISTRIBUIDOR, que estão há mais de 60 dias sem comprar | 15 dias | Frequência quinzenal |
| Compra com regularidade | Clientes com frequência histórica de compra de menos de 7 dias que estão há mais de 10 dias sem comprar com qualquer vendedor da empresa | 21 dias | Distribuidores ativos só entram se nunca compraram no grupo ou compraram nos últimos 60 dias |
| Bloqueio: distribuidor com vendas em 60 dias | Clientes ativos para o vendedor, do ramo DISTRIBUIDOR, que nunca compraram no grupo de vendedores ou compraram nele nos últimos 60 dias | Não agendar | Com mais de 10 dias sem comprar na empresa, só se frequência histórica indefinida ou de pelo menos 7 dias |
| Ativos sem vendas em 30 dias | Clientes ativos para o vendedor, de ramo diferente de DISTRIBUIDOR, que estão há mais de 30 dias sem comprar no grupo de vendedores | 15 dias | Com mais de 10 dias sem comprar na empresa, só se frequência histórica indefinida ou de pelo menos 7 dias |
| Bloqueio: ativos com vendas em 30 dias | Clientes ativos para o vendedor, de ramo diferente de DISTRIBUIDOR, que nunca compraram no grupo de vendedores ou compraram nele nos últimos 30 dias | Não agendar | Com mais de 10 dias sem comprar na empresa, só se frequência histórica indefinida ou de pelo menos 7 dias |
| Inativos e prospects | Clientes não ativos para o vendedor, incluindo os que nunca compraram na empresa | 30 dias | Com mais de 10 dias sem comprar na empresa, só se frequência histórica indefinida ou de pelo menos 7 dias |

## Pontos de atenção

- O bloqueio 'Não agendar ramo distribuidor com vendas em 60 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram nas regras 'Ramo distribuidor sem vendas em 60 dias' e 'Compra com regularidade'.
- O bloqueio 'Não agendar ativos com vendas em 30 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram nas regras 'Ramo distribuidor sem vendas em 60 dias', 'Compra com regularidade' e 'Ativos e sem vendas em 30 dias'.
- A cascata mistura escopos de recência de compra (empresa: Compra com regularidade; grupo: Ramo distribuidor sem vendas em 60 dias e Ativos e sem vendas em 30 dias), então as faixas podem se sobrepor ou deixar lacunas.
