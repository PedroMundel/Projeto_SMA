# regra_229.gobr

Regra de agendamento do time farm por tempo desde a última compra, com faixas para quem nunca comprou, quem está há mais de 60 dias sem comprar, quem está entre 30 e 60 dias sem comprar e quem só comprou fora do grupo de vendedores. Deixam de ser agendados os clientes que compraram nos últimos 30 dias. A última regra atende quem já comprou na empresa mas nunca com o grupo de vendedores.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram nos últimos 30 dias | Não agendar |  |
| Nunca compraram | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Cobertura mensal de positivação | Clientes que estão há mais de 60 dias sem comprar | 14 dias |  |
| Caminhando para inatividade | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 21 dias |  |
| Sem fidelidade | Clientes que já compraram com qualquer vendedor da empresa, mas nunca compraram no grupo de vendedores | 28 dias | Última regra: vale para quem sobrou das anteriores |

## Pontos de atenção

- O nome da regra 'Este cliente já não tem fidelidade com a sua empresa' fala em 90 dias, mas a regra usa outro valor.
