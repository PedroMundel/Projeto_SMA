# regra_081.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes ativos são atendidos a cada 7 dias, clientes inativos a cada 30 dias e clientes sem vendas a cada 30 dias, com preferência de segunda a sexta. A regra de não agendar inativos e inadimplentes e a regra de 21 dias para ativos inadimplentes nunca são aplicadas, pois esses clientes já são tratados pelas faixas anteriores.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos | Clientes ativos para o vendedor | 7 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor | 21 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Inativos | Clientes inativos para o vendedor | 30 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor | Não agendar | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Sem vendas | Clientes sem vendas para o vendedor | 30 dias | Preferência de atendimento de segunda a sexta; demais dias sem atendimento |

## Pontos de atenção

- A regra '21 dias para clientes ativos e inadimplentes' (R2) nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'nao agendar inativos e inadimplentes' (R4) nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- O bloqueio 'nao agendar inativos e inadimplentes' vem depois das faixas de frequência, então não bloqueia clientes que já entraram nelas.
