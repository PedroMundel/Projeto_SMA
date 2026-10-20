# regra_060.gobr

Regra padrão de frequência por situação do cliente, para os times de televendas e de campo. Em cada time, os clientes ativos têm frequência de 7 dias e os não ativos, 15 dias. No campo, as duas faixas têm parametrização fixa. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos (televendas) | Clientes ativos para o vendedor | 7 dias |  |
| Inativos (televendas) | Clientes não ativos para o vendedor | 15 dias |  |
| Ativos (campo) | Clientes ativos para o vendedor | 7 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |
| Inativos (campo) | Clientes não ativos para o vendedor | 15 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |

## Pontos de atenção

- O nome da regra 'Frequencia de 14 dias para clientes inativos (campo)' fala em 14 dias, mas a regra usa 15 dias.
