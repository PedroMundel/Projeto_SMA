# regra_151.gobr

Regra de não agendamento para clientes de campo em ruptura (sem compra há entre 7 e 60 dias) transferidos para o time de televendas. A única regra bloqueia os clientes da segmentação de ruptura que compraram nos últimos 60 dias e só é executada na última semana do mês. O arquivo não traz regra de frequência.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas fixa com ruptura de campo | Clientes do time de campo em ruptura, sem compra há entre 7 e 60 dias, transferidos para televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: ativos de campo com vendas em 60 dias | Clientes da segmentação 'cliente de ruptura', que compraram nos últimos 60 dias | Não agendar | Executada somente na última semana do mês |

## Pontos de atenção

- Todos os clientes da carteira 'televendas fixa com ruptura de campo' não se enquadram em nenhuma regra e ficam sem parametrização.
