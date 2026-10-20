# regra_170.gobr

Agendamento para todos os vendedores, organizado por ramo de atividade (distribuidor ou não), situação de ativo para o vendedor, tempo sem comprar e frequência histórica de compra. As frequências são de 15, 21 e 30 dias. Deixam de ser agendados os distribuidores ativos com vendas em 60 dias e os demais ativos com vendas em 30 dias. A regra final atende inativos e prospects a cada 30 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Distribuidores sem vendas em 60 dias | Clientes ativos para o vendedor, do ramo DISTRIBUIDOR, que estão há mais de 60 dias sem comprar | 15 dias |  |
| Compra com regularidade | Clientes sem comprar na empresa há mais de 10 dias e com frequência histórica de compra de menos de 7 dias, exceto os já tratados pela regra anterior | 21 dias |  |
| Bloqueio: distribuidor com vendas em 60 dias | Clientes ativos para o vendedor, do ramo DISTRIBUIDOR, que nunca compraram ou compraram no grupo de vendedores nos últimos 60 dias, exceto os já tratados pelas regras anteriores | Não agendar |  |
| Ativos sem vendas em 30 dias | Clientes ativos para o vendedor, de ramo diferente de DISTRIBUIDOR, sem comprar no grupo de vendedores há mais de 30 dias, exceto os já tratados pelas regras anteriores | 15 dias |  |
| Bloqueio: ativos com vendas em 30 dias | Clientes ativos para o vendedor, de ramo diferente de DISTRIBUIDOR, que nunca compraram ou compraram no grupo de vendedores nos últimos 30 dias, exceto os já tratados pelas regras anteriores | Não agendar |  |
| Inativos e prospects | Clientes não ativos para o vendedor, incluindo os que nunca compraram, exceto os já tratados pelas regras anteriores | 30 dias | Regra final: vale para quem sobrou das regras anteriores |

## Pontos de atenção

- O bloqueio 'Não agendar ramo distribuidor com vendas em 60 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Ramo distribuidor sem vendas em 60 dias' e 'Compra com regularidade'.
- O bloqueio 'Não agendar ativos com vendas em 30 dias' vem depois das faixas de frequência, então não bloqueia clientes que já entraram em 'Ramo distribuidor sem vendas em 60 dias', 'Compra com regularidade' e 'Ativos e sem vendas em 30 dias'.
- As faixas misturam escopos de tempo sem compra (na empresa toda em 'Compra com regularidade'; no grupo de vendedores em 'Ramo distribuidor sem vendas em 60 dias' e 'Ativos e sem vendas em 30 dias'), então podem se sobrepor ou deixar lacunas.
