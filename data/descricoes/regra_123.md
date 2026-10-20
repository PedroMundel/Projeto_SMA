# regra_123.gobr

Regra de frequência para três grupos: televendas, time de saúde do televendas (vendedores de id 7027) e campo. Em cada um, clientes ativos para o vendedor são atendidos a cada 7 dias e os não ativos a cada 15 dias. No time de saúde só entram clientes do ramo de atividade de id 1, e os demais ramos não são agendados. No campo, a frequência e os dias são fixos para o gerador de agendas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos (televendas) | Clientes ativos para o vendedor | 7 dias |  |
| Inativos (televendas) | Clientes que não estão ativos para o vendedor | 15 dias |  |
| Ativos (saúde) | Clientes com ramo de atividade (id) igual a 1 e ativos para o vendedor | 7 dias |  |
| Inativos (saúde) | Clientes com ramo de atividade (id) igual a 1 e que não estão ativos para o vendedor | 15 dias |  |
| Bloqueio: ramo diferente de saúde | Clientes com ramo de atividade (id) diferente de 1 | Não agendar |  |
| Ativos (campo) | Clientes ativos para o vendedor | 7 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |
| Inativos (campo) | Clientes que não estão ativos para o vendedor | 15 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |

## Pontos de atenção

- O nome da regra 'Frequencia de 14 dias para clientes inativos (campo)' fala em 14 dias, mas a regra usa 15 dias.
