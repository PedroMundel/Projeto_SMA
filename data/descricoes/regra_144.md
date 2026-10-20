# regra_144.gobr

Regra de frequência por situação do cliente, aplicada a todos os vendedores: prospects, inadimplentes, primeira compra, compra entre 31 e 60 dias, risco de inatividade e inativos. Nenhuma regra bloqueia a agenda. As duas últimas regras tratam quem comprou nos últimos 30 dias, com frequência de 21 dias para Fabricantes e Segmentos de Revendas/Manutenção e de 28 dias para os times de consumidor final.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Inadimplentes | Clientes inadimplentes que já compraram na empresa | 21 dias |  |
| Boas-vindas ao primeiro pedido | Clientes adimplentes com uma única compra na empresa, cadastrados no ERP há pelo menos 30 dias | 28 dias |  |
| Compra entre 31 e 60 dias | Clientes adimplentes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 30 dias | Compra única só entra se cadastrado no ERP há menos de 30 dias |
| Em ruptura: risco de inatividade | Clientes adimplentes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 10 dias | Compra única só entra se cadastrado no ERP há menos de 30 dias |
| Inativos: resgate | Clientes adimplentes inativos na empresa que nunca compraram no grupo de vendedores, compraram nele nos últimos 30 dias ou estão há mais de 90 dias sem comprar nele | 21 dias | Compra única só entra se cadastrado no ERP há menos de 30 dias |
| Ativos: Fabricantes e Revendas/Manutenção | Clientes que compraram nos últimos 30 dias | 21 dias | Vale para os times Fabricantes e Segmentos de Revendas/Manutenção |
| Ativos: Consumidor final | Clientes que compraram nos últimos 30 dias | 28 dias | Vale para os times Consumidor final recorrente, Compra esporádica e Consumidor final - Grande porte |

## Pontos de atenção

- Clientes adimplentes que já compraram na empresa, fora do ciclo de vida inativo, e que nunca compraram no grupo de vendedores, compraram nele nos últimos 30 dias ou estão há mais de 90 dias sem comprar nele não se enquadram em nenhuma regra do time todos e ficam sem parametrização (compra única só se cadastrados há menos de 30 dias).
- Clientes dos times Fabricantes e Segmentos de Revendas/Manutenção que nunca compraram ou estão há mais de 30 dias sem comprar não se enquadram em nenhuma regra desses times e ficam sem parametrização.
- Clientes dos times Consumidor final recorrente, Compra esporádica e Consumidor final - Grande porte que nunca compraram ou estão há mais de 30 dias sem comprar não se enquadram em nenhuma regra desses times e ficam sem parametrização.
