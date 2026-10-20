# regra_160.gobr

Regra de frequência para dois times: os vendedores ativos (televendas habilitados, exceto quatro vendedores) e os vendedores prospects (esses quatro vendedores). As seis primeiras regras tratam o fechamento de rota, com frequência de 1 dia para pessoas jurídicas com rota nos próximos 1 dia e sem visita há mais de 3 dias. Depois vêm a primeira compra (7 dias para prospects, 14 para ativos) e as faixas por tempo sem comprar; pessoas físicas ficam em 14 dias. Não há bloqueios.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Fechamento de rota: primeira compra | Clientes pessoa jurídica sem vendas para o vendedor | 1 dia | Rota nos próximos 1 dia; visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: estimular regularidade | Clientes pessoa jurídica que compraram com o próprio vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 1 dia | Rota nos próximos 1 dia; visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: risco de inatividade | Clientes pessoa jurídica que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 1 dia | Rota nos próximos 1 dia; visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: compra regularmente | Clientes pessoa jurídica que compraram com o próprio vendedor nos últimos 30 dias | 1 dia | Rota nos próximos 1 dia; visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: resgate | Clientes pessoa jurídica inativos para o vendedor que nunca compraram com ele ou estão há mais de 90 dias sem comprar | 1 dia | Rota nos próximos 1 dia; visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: ativos sem compra recente | Clientes pessoa jurídica ativos para o vendedor que nunca compraram com ele ou estão há mais de 90 dias sem comprar | 1 dia | Rota nos próximos 1 dia; visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Primeira compra (vendedores prospects) | Clientes pessoa jurídica sem vendas para o vendedor | 7 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
| Primeira compra (vendedores ativos) | Clientes pessoa jurídica sem vendas para o vendedor | 14 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
| Risco de inatividade | Clientes pessoa jurídica que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
| Estimular regularidade de compra | Clientes pessoa jurídica que compraram com o próprio vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
| Compra regularmente | Clientes pessoa jurídica que compraram com o próprio vendedor nos últimos 30 dias | 14 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
| Resgate de cliente sem compra | Clientes pessoa jurídica inativos para o vendedor que nunca compraram com ele ou estão há mais de 90 dias sem comprar | 21 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
| Pessoa física | Clientes pessoa física | 14 dias |  |
| Pessoa física/jurídica (indefinido) | Clientes pessoa jurídica ativos para o vendedor que nunca compraram com ele ou estão há mais de 90 dias sem comprar | 14 dias | Rota nos próximos 1 dia: nunca visitados, visitados nos últimos 3 dias ou sem visita há mais de 3000 dias |
