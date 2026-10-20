# regra_216.gobr

Regra de agendamento do time televendas dividida em três carteiras fixas por ramo de atividade: construtora, matcon e demais_segment. Todas começam pelos clientes que nunca compraram com o vendedor e pelos de compra única, seguem com faixas de regularidade, caminho para inatividade, resgate e requalificação, com frequências diferentes por carteira. Não há bloqueios de agenda. Três faixas das construtoras (inatividade, resgate e requalificação) nunca são aplicadas.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores do time televendas, filtrada por uma lista de ramos de atividade |
| matcon | Carteira fixa dos vendedores do time televendas, filtrada por uma lista de ramos de atividade |
| demais_segment | Carteira fixa dos vendedores do time televendas, com os clientes de ramos de atividade fora de uma lista definida |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos clientes (todos os segmentos) | Clientes das carteiras construtora, matcon e demais_segment que nunca compraram com o próprio vendedor | 7 dias |  |
| Novo cliente (Construtoras) | Clientes da carteira construtora que já compraram com o próprio vendedor e têm uma única compra com ele | 14 dias |  |
| Novo cliente (exceto Construtoras) | Clientes das carteiras matcon e demais_segment que já compraram com o próprio vendedor e têm uma única compra com ele | 7 dias |  |
| Compra com regularidade (exceto Construtoras) | Clientes que compraram no grupo de vendedores nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar, com mais de uma compra com o vendedor | Pelo histórico, mínimo de 7 e máximo de 30 dias | Carteiras matcon e demais_segment |
| Construtoras com venda em 30 dias | Clientes que compraram no grupo de vendedores nos últimos 30 dias, com mais de uma compra com o vendedor | 7 dias | Carteira construtora |
| Construtoras sem venda em 30 dias | Clientes sem comprar no grupo de vendedores há mais de 30 dias, com mais de uma compra com o vendedor | 14 dias | Carteira construtora |
| Estimular regularidade (Matcon) | Clientes que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar, com mais de uma compra com o vendedor | 7 dias | Exige compra no grupo de vendedores nos últimos 6 dias ou mais de 30 dias sem comprar no grupo |
| Estimular regularidade (exceto Matcon) | Clientes da carteira demais_segment que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar, com mais de uma compra com o vendedor | 14 dias | Exige compra no grupo de vendedores nos últimos 6 dias ou mais de 30 dias sem comprar no grupo |
| Caminhando para inatividade (Matcon) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra com o vendedor | 7 dias |  |
| Caminhando para inatividade (Construtoras) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Caminhando para inatividade (exceto Matcon e Construtoras) | Clientes da carteira demais_segment que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra com o vendedor | 21 dias |  |
| Resgate de inativos (Matcon) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar, com mais de uma compra com o vendedor | 7 dias |  |
| Resgate de inativos (Construtoras) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Resgate de inativos (exceto Matcon e Construtoras) | Clientes da carteira demais_segment que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar, com mais de uma compra com o vendedor | 14 dias |  |
| Requalificar e resgatar (exceto Construtoras) | Clientes sem comprar na empresa há mais de 180 dias, com mais de uma compra com o vendedor | 14 dias | Carteiras matcon e demais_segment |
| Requalificar e resgatar (Construtoras) | Clientes sem comprar na empresa há mais de 180 dias | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Atenção!!! Cliente caminhando para inatividade! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Resgate este cliente inativo! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Requalifique e resgate este cliente! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A sequência de regras mistura escopos de recência de compra (empresa toda: as três faixas 'Estimule a regularidade de compra' (Matcon e Exceto Matcon) e 'Caminhando para inatividade' (Matcon); grupo de vendedores: as três faixas 'Cliente que compra com regularidade'). Faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes das carteiras construtora, matcon e demais_segment que compraram na empresa nos últimos 29 dias ou compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, que compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, e têm mais de uma compra com o vendedor, não se enquadram em nenhuma regra e ficam sem parametrização.
