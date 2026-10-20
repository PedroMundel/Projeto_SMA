# regra_148.gobr

Regra padrão de frequência do time de televendas, organizada pela situação do cliente para o vendedor: ativos, inativos e sem vendas. Clientes inadimplentes deixam de ser agendados. Ativos são atendidos a cada 7 dias; inativos e clientes sem vendas, a cada 15 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Ativos | Clientes ativos para o vendedor | 7 dias |  |
| Inativos | Clientes inativos para o vendedor | 15 dias |  |
| Sem vendas | Clientes que nunca compraram com o vendedor | 15 dias |  |

## Pontos de atenção

- O nome da regra 'Frequencia de 14 dias para clientes sem vendas' fala em 14 dias, mas a regra usa outro valor (15 dias).
