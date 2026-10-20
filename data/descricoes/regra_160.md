# regra_160.gobr

Regras de frequência dos times vendedores_ativos e vendedores_prospects. As seis primeiras faixas tratam o fechamento de rota, com frequência de 1 dia para pessoas jurídicas com rota nos próximos 1 dia e sem visita há mais de 3 dias, separadas por perfil de compra. As demais faixas organizam os clientes por tempo sem comprar (30, 60 e 90 dias) e pela primeira compra, que tem 7 dias para prospects e 14 dias para ativos. Pessoa física e tipo de pessoa indefinido fecham as regras. Não há bloqueios.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Fechamento de rota: primeira compra | Clientes pessoa jurídica sem vendas para o vendedor, com data de rota nos próximos 1 dia | 1 dia | Visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: estimular regularidade | Clientes pessoa jurídica que compraram com o vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, com data de rota nos próximos 1 dia | 1 dia | Visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: risco de inatividade | Clientes pessoa jurídica que compraram com o vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, com data de rota nos próximos 1 dia | 1 dia | Visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: compra regularmente | Clientes pessoa jurídica que compraram com o vendedor nos últimos 30 dias, com data de rota nos próximos 1 dia | 1 dia | Visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: resgate sem compra | Clientes pessoa jurídica inativos para o vendedor, há mais de 90 dias sem comprar com ele, com data de rota nos próximos 1 dia | 1 dia | Visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Fechamento de rota: demais ativos | Clientes pessoa jurídica ativos para o vendedor, há mais de 90 dias sem comprar com ele, com data de rota nos próximos 1 dia | 1 dia | Visitados nos últimos 3000 dias, mas sem visita há mais de 3 dias |
| Primeira compra (prospects) | Clientes pessoa jurídica sem vendas para o vendedor, exceto os já tratados pelo fechamento de rota da primeira compra | 7 dias | Vale para o time vendedores_prospects |
| Primeira compra (ativos) | Clientes pessoa jurídica sem vendas para o vendedor, exceto os já tratados pelo fechamento de rota da primeira compra | 14 dias | Vale para o time vendedores_ativos |
| Risco de inatividade | Clientes pessoa jurídica que compraram com o vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar, exceto os já tratados no fechamento de rota | 7 dias |  |
| Estimular regularidade de compra | Clientes pessoa jurídica que compraram com o vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar, exceto os já tratados no fechamento de rota | 14 dias |  |
| Compra regularmente | Clientes pessoa jurídica que compraram com o vendedor nos últimos 30 dias, exceto os já tratados no fechamento de rota | 14 dias |  |
| Resgate de cliente sem compra | Clientes pessoa jurídica inativos para o vendedor, há mais de 90 dias sem comprar com ele, exceto os já tratados pelas regras anteriores | 21 dias |  |
| Pessoa física | Clientes pessoa física | 14 dias |  |
| Tipo de pessoa indefinido | Clientes sem tipo de pessoa definido ou pessoas jurídicas ativas há mais de 90 dias sem comprar com o vendedor, exceto os já tratados pelas regras anteriores | 14 dias | Regra final: vale para quem sobrou das anteriores |
