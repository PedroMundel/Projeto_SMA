# regra_136.gobr

Regra de agendamento para os times capital e interior, cada um com sua carteira fixa. Clientes ativos para o vendedor têm frequência de 7 dias na capital e de 14 dias no interior. Não são agendados os clientes do ramo de atividade 19 (Funcionários) e os clientes não ativos de cada carteira.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira capital | Carteira fixa dos vendedores do time capital |
| carteira interior | Carteira fixa dos vendedores do time interior |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: ramo de atividade 19 (Funcionários) | Clientes do ramo de atividade (id) 19 | Não agendar |  |
| Ativos (Capital) | Clientes ativos para o vendedor | 7 dias |  |
| Bloqueio: inativos (Capital) | Clientes que não estão ativos para o vendedor | Não agendar |  |
| Ativos (Interior) | Clientes ativos para o vendedor | 14 dias |  |
| Bloqueio: inativos (Interior) | Clientes que não estão ativos para o vendedor | Não agendar |  |

## Pontos de atenção

- Para o time empresa toda, todos os clientes não se enquadram em nenhuma regra e ficam sem parametrização.
