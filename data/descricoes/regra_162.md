# regra_162.gobr

Regra de agendamento do time de televendas por histórico de compra do cliente. Antes das faixas, deixam de ser agendados os clientes pessoa física (CPF) e os inadimplentes. Clientes sem histórico e inativos têm 14 dias, quem está há mais de 45 dias sem comprar tem 30 dias, e a regra final usa a frequência do histórico de compras.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física (CPF) | Clientes pessoa física | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Sem histórico de compra | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Inativos | Clientes que já compraram com qualquer vendedor da empresa e estão inativos para o vendedor | 14 dias |  |
| Mais de 45 dias sem compra | Clientes que estão há mais de 45 dias sem comprar e não estão inativos para o vendedor | 30 dias |  |
| Frequência do histórico | Clientes que já compraram na empresa, não estão inativos para o vendedor e nunca compraram no grupo de vendedores ou compraram nele nos últimos 45 dias | Pelo histórico; se não houver, no mínimo 14 e no máximo 45 dias | Regra final: vale para quem sobrou das faixas anteriores |
