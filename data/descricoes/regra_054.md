# regra_054.gobr

Regra padrão aplicada à carteira fixa de todos os vendedores da empresa. Clientes sem vendas para o vendedor são agendados a cada 14 dias, e os adimplentes que já compraram, a cada 30 dias. Clientes inadimplentes que já compraram não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Sem vendas | Clientes sem vendas para o vendedor | 14 dias |  |
| Adimplentes | Clientes adimplentes e com alguma venda para o vendedor, ativos ou inativos | 30 dias |  |
| Bloqueio: inadimplentes | Clientes inadimplentes e com alguma venda para o vendedor, ativos ou inativos | Não agendar |  |

## Pontos de atenção

- O bloqueio 'Não agendar inadimplentes' vem depois da faixa de 14 dias para clientes sem venda, então não bloqueia clientes que já entraram nela.
