# regra_216.gobr

Regra de agendamento do time de televendas dividida em três carteiras fixas dos vendedores: construtora, matcon e demais_segment. Os clientes são organizados por compra única, regularidade e tempo sem comprar na empresa, com frequências de 7, 14, 21 e 28 dias, e não há bloqueios. As regras de construtora para inatividade, resgate e requalificação nunca são aplicadas, e a requalificação de quem passou de 180 dias sem comprar é feita pelas demais carteiras.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores do time televendas, filtrada por ramos de atividade |
| matcon | Carteira fixa dos vendedores do time televendas, filtrada por ramos de atividade |
| demais_segment | Carteira fixa dos vendedores do time televendas, com os ramos de atividade fora dos listados |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novo cliente (todos os segmentos) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Vale para as carteiras construtora, matcon e demais_segment |
| Novo cliente (construtoras) | Clientes que já compraram com o próprio vendedor, mas têm uma única compra com ele | 14 dias | Carteira construtora |
| Novo cliente (exceto construtoras) | Clientes que já compraram com o próprio vendedor, mas têm uma única compra com ele | 7 dias | Carteiras matcon e demais_segment |
| Compra com regularidade (exceto construtoras) | Clientes com mais de uma compra que compraram no grupo de vendedores nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar | Pelo histórico, entre 7 e 30 dias | Carteiras matcon e demais_segment |
| Compra com regularidade (construtoras, venda em 30 dias) | Clientes com mais de uma compra que compraram no grupo de vendedores nos últimos 30 dias | 7 dias | Carteira construtora |
| Compra com regularidade (construtoras, sem venda em 30 dias) | Clientes com mais de uma compra que estão há mais de 30 dias sem comprar no grupo de vendedores | 14 dias | Carteira construtora |
| Estimular regularidade (matcon) | Clientes com mais de uma compra que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar | 7 dias | Exige compra no grupo nos últimos 6 dias ou mais de 30 dias sem comprar nele. |
| Estimular regularidade (exceto matcon) | Clientes com mais de uma compra que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar | 14 dias | Exige compra no grupo nos últimos 6 dias ou mais de 30 dias sem comprar nele. Na prática, só demais_segment. |
| Caminhando para inatividade (matcon) | Clientes com mais de uma compra que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar | 7 dias | Carteira matcon |
| Caminhando para inatividade (construtoras) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Caminhando para inatividade (demais_segment) | Clientes com mais de uma compra que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar | 21 dias | Carteira demais_segment |
| Resgate de inativos (matcon) | Clientes com mais de uma compra que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 7 dias | Carteira matcon |
| Resgate de inativos (construtoras) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Resgate de inativos (demais_segment) | Clientes com mais de uma compra que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 14 dias | Carteira demais_segment |
| Requalificação (exceto construtoras) | Clientes com mais de uma compra que estão há mais de 180 dias sem comprar na empresa | 14 dias | Carteiras matcon e demais_segment |
| Requalificação (construtoras) | Clientes que estão há mais de 180 dias sem comprar na empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Atenção!!! Cliente caminhando para inatividade! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Resgate este cliente inativo! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Requalifique e resgate este cliente! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A cascata mistura escopos de recência de compra (empresa nas regras 'Estimule a regularidade...' e 'Atenção!!! ... (Matcon)', grupo de vendedores nas regras 'Cliente que compra com regularidade!'), então as faixas não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Nas carteiras construtora, matcon e demais_segment, clientes com mais de uma compra que compraram na empresa nos últimos 29 dias, ou nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo nos últimos 6 dias ou estão há mais de 30 dias sem comprar nele, não se enquadram em nenhuma regra e ficam sem parametrização.
