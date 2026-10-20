# regra_144.gobr

Regras de frequência por situação do cliente. O time todos organiza prospects, inadimplentes, primeira compra, compra entre 31 e 60 dias, risco de inatividade e resgate de inativos. Os times fabricantes e segmentos de revendas/manutenção têm uma regra de ativos com 21 dias, e os times de consumidor final, compra exporádica e grande porte têm outra com 28 dias. Nenhuma regra bloqueia a agenda.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias | Vale para o time todos |
| Inadimplentes | Clientes inadimplentes que já compraram com qualquer vendedor da empresa | 21 dias | Vale para o time todos |
| Boas-vindas ao primeiro pedido | Clientes adimplentes com uma única compra na empresa, cadastrados no ERP há pelo menos 30 dias | 28 dias | Vale para o time todos |
| Compra entre 31 e 60 dias | Clientes adimplentes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar (compra única só se cadastrados há menos de 30 dias) | 30 dias | Vale para o time todos |
| Risco de inatividade | Clientes adimplentes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar (compra única só se cadastrados há menos de 30 dias) | 10 dias | Vale para o time todos |
| Inativos: resgate | Clientes adimplentes inativos na empresa que nunca compraram no grupo de vendedores, compraram nele nos últimos 30 dias ou estão há mais de 90 dias sem comprar nele | 21 dias | Vale para o time todos; compra única só se cadastrados há menos de 30 dias |
| Ativos: Fabricantes e Revendas/Manutenção | Clientes que compraram nos últimos 30 dias | 21 dias | Vale para os times fabricantes e segmentos de revendas/manutenção |
| Ativos: Consumidor final | Clientes que compraram nos últimos 30 dias | 28 dias | Vale para os times consumidor final recorrente, compra exporadica e consumidor final - grande porte |

## Pontos de atenção

- Clientes do time todos que já compraram na empresa, são adimplentes, não estão no ciclo de vida inativo e nunca compraram no grupo de vendedores, compraram nele nos últimos 30 dias ou estão há mais de 90 dias sem comprar nele não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes dos times fabricantes e segmentos de revendas/manutenção que nunca compraram ou estão há mais de 30 dias sem comprar não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes dos times consumidor final recorrente, compra exporadica e consumidor final - grande porte que nunca compraram ou estão há mais de 30 dias sem comprar não se enquadram em nenhuma regra e ficam sem parametrização.
