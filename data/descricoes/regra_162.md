# regra_162.gobr

Regra de agendamento do time televendas por histórico de compra. Clientes pessoa física e inadimplentes não são agendados. Clientes sem histórico de compra e inativos têm frequência de 14 dias, quem está há mais de 45 dias sem comprar tem 30 dias, e a regra final segue o histórico de visitas, entre 14 e 45 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física | Clientes pessoa física | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Sem histórico de compra | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Inativos | Clientes que já compraram com a empresa e estão inativos para o vendedor | 14 dias |  |
| Mais de 45 dias sem comprar | Clientes que estão há mais de 45 dias sem comprar e não são inativos para o vendedor | 30 dias |  |
| Frequência pelo histórico | Clientes que já compraram com a empresa e não são inativos para o vendedor, e que nunca compraram no grupo de vendedores ou compraram nele nos últimos 45 dias | Pelo histórico, entre 14 e 45 dias |  |
