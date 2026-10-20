# regra_234.gobr

Regra de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes com queda de faturamento maior que 5% têm frequência de 3 dias; os demais seguem a média da empresa para ativos ou inativos, com atendimento em todos os dias da semana. Deixa de ser agendado quem está há pelo menos 1138 dias sem comprar. A regra final, de 7 dias, nunca é aplicada.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Queda de faturamento | Clientes com queda de faturamento maior que 5% | 3 dias |  |
| Bloqueio: mais de 1138 dias sem comprar | Clientes que compraram nos últimos 9999 dias, mas estão há pelo menos 1138 dias sem comprar, exceto os com queda de faturamento maior que 5% | Não agendar |  |
| Teste cidade Goiânia | Clientes da cidade de GOIANIA, exceto os com queda de faturamento maior que 5% | Média dos inativos da empresa | Dias de preferência: segunda a domingo |
| Clientes ativos | Clientes ativos para o vendedor, de cidades diferentes de GOIANIA, exceto os com queda de faturamento maior que 5% | Média dos ativos da empresa | Dias de preferência: segunda a domingo |
| Clientes inativos | Clientes inativos para o vendedor, de cidades diferentes de GOIANIA, exceto os com queda de faturamento maior que 5% | Média dos inativos da empresa | Dias de preferência: segunda a domingo |
| Clientes sem vendas | Clientes sem vendas para o vendedor, de cidades diferentes de GOIANIA, exceto os com queda de faturamento maior que 5% | Média dos inativos da empresa | Dias de preferência: segunda a domingo |
| Regra padrão (default) | Clientes de todos os grupos (sem filtro) | 7 dias | Nunca é aplicada: todos esses clientes já foram tratados antes. Atendimento preferencial de segunda a sexta. |

## Pontos de atenção

- O bloqueio 'Nao agendar quem esta a mais de 1138 dias sem comprar' vem depois da regra de 3 dias para queda de faturamento, então não bloqueia clientes que já entraram nela.
- A regra 'Regra Padrao - default' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
