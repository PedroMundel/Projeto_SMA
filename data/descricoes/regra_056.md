# regra_056.gobr

Regra com duas carteiras fixas: o time de prospecção e os demais vendedores da empresa. A prospecção atende clientes sem vendas a cada 30 dias e não agenda quem já comprou. Os demais vendedores atendem adimplentes ativos a cada 14 dias e adimplentes inativos, ativos inadimplentes e clientes sem vendas a cada 30 dias, com preferência de dias do vendedor. Inativos inadimplentes não são agendados.

## Carteiras

| Carteira | Descrição |
|---|---|
| regra padrao | Carteira fixa de todos os vendedores, exceto os do time de prospecção |
| carteira prospec | Carteira fixa dos vendedores do time de prospecção |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospecção: sem vendas | Clientes sem vendas para o vendedor | 30 dias | Respeita a preferência de dias configurada pelo vendedor |
| Bloqueio: clientes que já compraram (prospecção) | Clientes com alguma venda (ativos ou inativos) para o vendedor, exceto os já tratados pelas regras anteriores | Não agendar |  |
| Adimplentes ativos | Clientes adimplentes e ativos para o vendedor | 14 dias | Respeita a preferência de dias configurada pelo vendedor |
| Adimplentes inativos | Clientes adimplentes e inativos para o vendedor | 30 dias | Respeita a preferência de dias configurada pelo vendedor |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 30 dias | Respeita a preferência de dias configurada pelo vendedor |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem vendas | Clientes sem vendas para o vendedor | 30 dias | Respeita a preferência de dias configurada pelo vendedor |
