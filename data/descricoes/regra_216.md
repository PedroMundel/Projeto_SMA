# regra_216.gobr

Regra de agendamento do time de televendas, organizada em três carteiras por ramo de atividade: construtora, matcon e demais_segment. Clientes que nunca compraram com o próprio vendedor são atendidos a cada 7 dias; os de compra única, a cada 14 ou 7 dias conforme a carteira; os demais seguem faixas de tempo sem comprar (30, 60, 89, 179 e 180 dias). Nenhuma regra bloqueia a agenda, e três regras da carteira construtora nunca são aplicadas.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores de televendas com clientes de ramos de atividade de construtoras |
| matcon | Carteira fixa dos vendedores de televendas com clientes de ramos de atividade de materiais de construção |
| demais_segment | Carteira fixa dos vendedores de televendas com os clientes dos demais ramos de atividade, fora das duas carteiras anteriores |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos clientes (todos os segmentos) | Clientes das carteiras construtora, matcon e demais_segment que nunca compraram com o próprio vendedor | 7 dias |  |
| Novos clientes: construtoras | Clientes da carteira construtora que já compraram com o próprio vendedor, com uma única compra | 14 dias |  |
| Novos clientes: exceto construtoras | Clientes das carteiras matcon e demais_segment que já compraram com o próprio vendedor, com uma única compra | 7 dias |  |
| Regulares: exceto construtoras | Clientes de matcon e demais_segment que compraram no grupo de vendedores nos últimos 30 dias, parados há pelo menos 7 dias, com mais de uma compra com o vendedor | Pelo histórico, entre 7 e 30 dias | Sem histórico de compras, a frequência fica limitada a no mínimo 7 e no máximo 30 dias |
| Regulares: construtoras com venda em 30 dias | Clientes da carteira construtora que compraram no grupo de vendedores nos últimos 30 dias e têm mais de uma compra com o próprio vendedor | 7 dias |  |
| Regulares: construtoras sem venda em 30 dias | Clientes da carteira construtora que estão há mais de 30 dias sem comprar no grupo de vendedores e têm mais de uma compra com o próprio vendedor | 14 dias |  |
| Estímulo à regularidade: matcon | Clientes da carteira matcon, com mais de uma compra com o vendedor, que compraram na empresa nos últimos 60 dias e estão há pelo menos 30 dias sem comprar | 7 dias | Também exige compra no grupo de vendedores nos últimos 6 dias ou mais de 30 dias sem comprar no grupo |
| Estímulo à regularidade: exceto matcon | Clientes da carteira demais_segment, com mais de uma compra com o vendedor, que compraram na empresa nos últimos 60 dias e estão há pelo menos 30 dias sem comprar | 14 dias | Também exige compra no grupo de vendedores nos últimos 6 dias ou mais de 30 dias sem comprar no grupo |
| Caminhando para inatividade: matcon | Clientes da carteira matcon, com mais de uma compra com o vendedor, que compraram na empresa nos últimos 89 dias e estão há mais de 60 dias sem comprar | 7 dias |  |
| Caminhando para inatividade: construtoras | Clientes da carteira construtora que compraram na empresa nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Caminhando para inatividade: demais segmentos | Clientes da carteira demais_segment, com mais de uma compra com o vendedor, que compraram na empresa nos últimos 89 dias e estão há mais de 60 dias sem comprar | 21 dias |  |
| Resgate de inativos: matcon | Clientes da carteira matcon, com mais de uma compra com o vendedor, que compraram na empresa nos últimos 179 dias e estão há mais de 89 dias sem comprar | 7 dias |  |
| Resgate de inativos: construtoras | Clientes da carteira construtora que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Resgate de inativos: demais segmentos | Clientes da carteira demais_segment, com mais de uma compra com o vendedor, que compraram na empresa nos últimos 179 dias e estão há mais de 89 dias sem comprar | 14 dias |  |
| Requalificação: exceto construtoras | Clientes das carteiras matcon e demais_segment, com mais de uma compra com o vendedor, que estão há mais de 180 dias sem comprar com a empresa | 14 dias |  |
| Requalificação: construtoras | Clientes da carteira construtora que estão há mais de 180 dias sem comprar com qualquer vendedor da empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Atenção!!! Cliente caminhando para inatividade! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Resgate este cliente inativo! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Requalifique e resgate este cliente! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- As regras misturam medidas de compra de escopos diferentes (empresa e grupo de vendedores), então as faixas não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes das carteiras construtora, matcon e demais_segment (limitados a demais_segment e matcon) que já compraram com o próprio vendedor sem compra única, compraram com qualquer vendedor da empresa nos últimos 29 dias ou nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes das carteiras matcon e demais_segment que já compraram com o próprio vendedor sem compra única, compraram com qualquer vendedor da empresa nos últimos 29 dias ou nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes da carteira matcon que já compraram com o próprio vendedor sem compra única, compraram com qualquer vendedor da empresa nos últimos 29 dias ou nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes das carteiras construtora e demais_segment (limitados a demais_segment) que já compraram com o próprio vendedor sem compra única, compraram com qualquer vendedor da empresa nos últimos 29 dias ou nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes da carteira demais_segment que já compraram com o próprio vendedor sem compra única, compraram com qualquer vendedor da empresa nos últimos 29 dias ou nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
