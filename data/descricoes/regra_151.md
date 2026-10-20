# regra_151.gobr

Regra de não agendamento da carteira fixa do televendas com clientes em ruptura do time de campo, transferidos para o televendas. Há uma única regra, que bloqueia a agenda de todos os clientes dessa carteira e é executada somente na última semana do mês. A segmentação 'cliente de ruptura' reúne a carteira fixa dos vendedores do time de campo que compraram nos últimos 60 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas fixa com ruptura de campo | Carteira fixa de clientes do time de campo em ruptura, sem compra há entre 7 e 60 dias, transferidos para o televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: ativos de campo | Clientes de todos os tipos da carteira televendas fixa com ruptura de campo | Não agendar | Executada somente na última semana do mês |

## Pontos de atenção

- O nome da regra 'Não agendar Ativos de campo com vendas em 60 dias' fala em 60 dias, mas a regra usa outro valor.
- Clientes da carteira 'televendas fixa com ruptura de campo' (todos os clientes) não se enquadram em nenhuma regra de frequência e ficam sem parametrização.
