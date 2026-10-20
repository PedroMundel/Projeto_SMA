# regra_179.gobr

Regra de agendamento do time televendas, dividida em três carteiras fixas por ramo de atividade: construtora, matcon e demais_segment. Os clientes são organizados em novos (nunca compraram com o vendedor ou com uma única compra), clientes com mais de uma compra com o vendedor por tempo sem comprar na empresa (até 60, 89 e 179 dias) e os parados há mais de 180 dias. Não há bloqueios de agenda, e as regras finais de cada carteira são de requalificação e resgate.

## Carteiras

| Carteira | Descrição |
|---|---|
| construtora | Carteira fixa dos vendedores do time televendas, com clientes de uma lista de ramos de atividade |
| matcon | Carteira fixa dos vendedores do time televendas, com clientes de uma lista de ramos de atividade |
| demais_segment | Carteira fixa dos vendedores do time televendas, com clientes de ramos de atividade fora de uma lista definida |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos clientes (todos os segmentos) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Carteiras construtora, matcon e demais_segment |
| Novos clientes (construtoras) | Clientes que já compraram com o próprio vendedor, em uma única compra | 14 dias | Carteira construtora |
| Novos clientes (exceto construtoras) | Clientes que já compraram com o próprio vendedor, em uma única compra | 7 dias | Carteiras matcon e demais_segment |
| Compra regular (exceto construtoras) | Clientes com mais de uma compra com o vendedor que compraram no grupo de vendedores nos últimos 30 dias, mas estão há pelo menos 7 dias sem comprar | Pelo histórico, entre 7 e 30 dias | Carteiras matcon e demais_segment |
| Compra regular (construtoras, com venda em 30 dias) | Clientes com mais de uma compra com o vendedor que compraram no grupo de vendedores nos últimos 30 dias | 7 dias | Carteira construtora |
| Compra regular (construtoras, sem venda em 30 dias) | Clientes com mais de uma compra com o vendedor que estão há mais de 30 dias sem comprar no grupo de vendedores | 14 dias | Carteira construtora |
| Estimular regularidade (matcon) | Clientes com mais de uma compra com o vendedor que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar | 7 dias | Carteira matcon; exige compra no grupo nos últimos 6 dias ou mais de 30 dias sem comprar no grupo |
| Estimular regularidade (exceto matcon) | Clientes com mais de uma compra com o vendedor que compraram na empresa nos últimos 60 dias, mas estão há pelo menos 30 dias sem comprar | 14 dias | Carteira demais_segment; exige compra no grupo nos últimos 6 dias ou mais de 30 dias sem comprar no grupo |
| Caminhando para inatividade (matcon) | Clientes com mais de uma compra com o vendedor que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar | 7 dias | Carteira matcon |
| Caminhando para inatividade (construtoras) | Clientes que compraram na empresa nos últimos 89 dias, mas estão há pelo menos 60 dias sem comprar | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Caminhando para inatividade (demais) | Clientes com mais de uma compra com o vendedor que compraram na empresa nos últimos 89 dias, mas estão há mais de 60 dias sem comprar | 21 dias | Carteira demais_segment |
| Resgate de inativos (matcon) | Clientes com mais de uma compra com o vendedor que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 7 dias | Carteira matcon |
| Resgate de inativos (construtoras) | Clientes que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Resgate de inativos (demais) | Clientes com mais de uma compra com o vendedor que compraram na empresa nos últimos 179 dias, mas estão há mais de 89 dias sem comprar | 14 dias | Carteira demais_segment |
| Requalificar e resgatar (exceto construtoras) | Clientes com mais de uma compra com o vendedor que estão há mais de 180 dias sem comprar na empresa | 14 dias | Carteiras matcon e demais_segment |
| Requalificar e resgatar (construtoras) | Clientes que estão há mais de 180 dias sem comprar na empresa | 28 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'Atenção!!! Cliente caminhando para inatividade! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores ('Ative um novo cliente em sua carteira! (Todos os segmentos)', 'Estabeleça relacionamento com seu novo cliente! (Construtoras)' e 'Cliente que compra com regularidade! (Construtoras sem venda em 30d)').
- A regra 'Resgate este cliente inativo! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores ('Ative um novo cliente em sua carteira! (Todos os segmentos)', 'Estabeleça relacionamento com seu novo cliente! (Construtoras)' e 'Cliente que compra com regularidade! (Construtoras sem venda em 30d)').
- A regra 'Requalifique e resgate este cliente! (Construtoras)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores ('Ative um novo cliente em sua carteira! (Todos os segmentos)', 'Estabeleça relacionamento com seu novo cliente! (Construtoras)' e 'Cliente que compra com regularidade! (Construtoras sem venda em 30d)').
- As faixas misturam medidas diferentes de última compra: na empresa toda ('Estimule a regularidade de compra do seu cliente! (Matcon)', '... (Exceto Matcon)' e 'Atenção!!! Cliente caminhando para inatividade! (Matcon)') e no grupo de vendedores ('Cliente que compra com regularidade! (Exceto Construtoras)', '... (Construtoras com venda em 30d)' e '... (Construtoras sem venda em 30d)'). Por isso as faixas podem se sobrepor ou deixar lacunas.
- Clientes das carteiras construtora, matcon e demais_segment (entre eles os das carteiras demais_segment e matcon) com mais de uma compra com o vendedor, que compraram na empresa nos últimos 29 dias ou que compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes das carteiras matcon e demais_segment com mais de uma compra com o vendedor, que compraram na empresa nos últimos 29 dias ou que compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes da carteira matcon com mais de uma compra com o vendedor, que compraram na empresa nos últimos 29 dias ou que compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes das carteiras construtora e demais_segment (entre eles os da carteira demais_segment) com mais de uma compra com o vendedor, que compraram na empresa nos últimos 29 dias ou que compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
- Clientes da carteira demais_segment com mais de uma compra com o vendedor, que compraram na empresa nos últimos 29 dias ou que compraram nos últimos 180 dias mas estão há mais de 179 dias sem comprar, e que compraram no grupo de vendedores nos últimos 6 dias ou estão há mais de 30 dias sem comprar no grupo, não se enquadram em nenhuma regra e ficam sem parametrização.
