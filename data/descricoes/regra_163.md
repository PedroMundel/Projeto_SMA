# regra_163.gobr

Regra de frequência do time televendas com duas carteiras fixas por ramo de atividade, construtora e matcom, cada uma com faixas próprias por tempo sem comprar e histórico de compras com o vendedor. Na carteira construtora, clientes que compraram nos últimos 30 dias não são agendados. A última regra de cada carteira nunca é aplicada.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores do time televendas, com os ramos de atividade (id) 15, 16, 3 e 6 |
| matcom | Carteira fixa dos vendedores do time televendas, com os ramos de atividade (id) fora de 15, 16, 3 e 6 |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: venda em 30 dias (Construtoras) | Clientes que compraram nos últimos 30 dias | Não agendar |  |
| Novo cliente (Construtoras) | Clientes que nunca compraram ou estão há mais de 30 dias sem comprar, sem vendas para o vendedor | 30 dias |  |
| Relacionamento com novo cliente (Construtoras) | Clientes que estão há mais de 60 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor e uma única compra com ele | 21 dias |  |
| Regularidade de compra (Construtoras) | Clientes que compraram com o vendedor nos últimos 30 dias ou estão há mais de 60 dias sem comprar com ele, e há mais de 30 dias sem comprar no grupo | 28 dias | Com compra única com o vendedor, só se o grupo comprou nos últimos 60 dias |
| Entrando em ruptura (Construtoras) | Clientes que compraram com o vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar com ele e no grupo | 14 dias | Com compra única com o vendedor, só se o grupo comprou nos últimos 60 dias |
| Manter cliente ativo (Construtoras) | Clientes da carteira construtora, sem filtro adicional | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Novo cliente (Matcom) | Clientes sem vendas para o vendedor | 7 dias |  |
| Relacionamento com novo cliente (Matcom) | Clientes que estão há mais de 30 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor e uma única compra com ele | 14 dias |  |
| Compra com regularidade (Matcom) | Clientes que compraram nos últimos 30 dias, mas estão há mais de 6 dias sem comprar, com alguma venda (ativos ou inativos) para o vendedor | Pelo histórico, entre 7 e 30 dias |  |
| Regularidade de compra (Matcom) | Clientes que compraram com o vendedor nos últimos 30 dias ou estão há mais de 60 dias sem comprar com ele, e compraram no grupo nos últimos 6 dias | 14 dias | Com mais de uma compra com o vendedor, vale também com grupo há mais de 30 dias sem comprar |
| Entrando em ruptura (Matcom) | Clientes que compraram com o vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, e compraram no grupo nos últimos 6 dias | 7 dias | Com mais de uma compra com o vendedor, vale também com grupo há mais de 30 dias sem comprar |
| Manter cliente ativo (Matcom) | Clientes da carteira matcom, sem filtro adicional | 7 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Garanta que este cliente se mantenha ativo (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Garanta que este cliente se mantenha ativo (Matcom)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A cascata mistura compras no grupo de vendedores e compras do próprio vendedor; as faixas podem se sobrepor ou deixar lacunas.
