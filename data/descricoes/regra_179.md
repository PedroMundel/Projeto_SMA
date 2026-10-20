# regra_179.gobr

Regra do time de televendas organizada em três carteiras fixas por ramo de atividade: construtora, matcon e demais_segment. Clientes que nunca compraram com o vendedor entram a cada 7 dias; os demais seguem faixas por carteira, de 7 a 28 dias, conforme compra única, regularidade, risco de inatividade e inatividade. Não há bloqueios. Três regras da carteira construtora nunca são aplicadas.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores de televendas para clientes de um grupo de ramos de atividade |
| matcon | Carteira fixa dos vendedores de televendas para clientes de um segundo grupo de ramos de atividade |
| demais_segment | Carteira fixa dos vendedores de televendas para clientes de ramos de atividade fora dos listados nas outras carteiras |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos clientes (todos os segmentos) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Vale para as três carteiras |
| Novos clientes (construtoras) | Clientes que já compraram com o próprio vendedor, mas apenas uma vez | 14 dias | Carteira construtora |
| Novos clientes (exceto construtoras) | Clientes que já compraram com o próprio vendedor, mas apenas uma vez | 7 dias | Carteiras matcon e demais_segment |
| Compra regular (exceto construtoras) | Clientes que compraram no grupo de vendedores nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar, com mais de uma compra com o vendedor | Pelo histórico, entre 7 e 30 dias | Carteiras matcon e demais_segment |
| Compra regular (construtoras, com venda em 30 dias) | Clientes que compraram no grupo de vendedores nos últimos 30 dias, com mais de uma compra com o vendedor | 7 dias | Carteira construtora |
| Compra regular (construtoras, sem venda em 30 dias) | Clientes que estão há mais de 30 dias sem comprar no grupo de vendedores, com mais de uma compra com o vendedor | 14 dias | Carteira construtora |
| Estímulo à regularidade (matcon) | Clientes que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar, com mais de uma compra com o vendedor | 7 dias | Vale para quem comprou no grupo nos últimos 6 dias ou está há mais de 30 dias sem comprar nele |
| Estímulo à regularidade (exceto matcon) | Clientes que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar, com mais de uma compra com o vendedor | 14 dias | Vale para quem comprou no grupo nos últimos 6 dias ou está há mais de 30 dias sem comprar nele |
| Caminhando para inatividade (matcon) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra com o vendedor | 7 dias |  |
| Caminhando para inatividade (construtoras) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Caminhando para inatividade (demais) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar, com mais de uma compra com o vendedor | 21 dias | Carteira demais_segment |
| Resgate de inativos (matcon) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar, com mais de uma compra com o vendedor | 7 dias |  |
| Resgate de inativos (construtoras) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Resgate de inativos (demais) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar, com mais de uma compra com o vendedor | 14 dias | Carteira demais_segment |
| Requalificação (exceto construtoras) | Clientes que estão há mais de 180 dias sem comprar na empresa, com mais de uma compra com o vendedor | 14 dias | Carteiras matcon e demais_segment |
| Requalificação (construtoras) | Clientes que estão há mais de 180 dias sem comprar na empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Atenção!!! Cliente caminhando para inatividade! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Resgate este cliente inativo! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Requalifique e resgate este cliente! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A sequência de regras mistura medidas de tempo sem comprar de escopos diferentes (empresa toda e grupo de vendedores); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes das carteiras construtora, matcon e demais_segment que compraram na empresa nos últimos 29 dias, ou compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo nos últimos 6 dias ou estão há mais de 30 dias sem comprar nele, com mais de uma compra com o vendedor, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes das carteiras matcon e demais_segment com essa mesma situação (compra na empresa nos últimos 29 dias, ou entre 179 e 180 dias sem comprar, e compra recente ou mais de 30 dias sem comprar no grupo) não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes da carteira matcon com essa mesma situação não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes das carteiras construtora e demais_segment com essa mesma situação não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes da carteira demais_segment com essa mesma situação não se enquadram em nenhuma regra e ficam sem parametrização.
