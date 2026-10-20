# regra_080.gobr

Regra padrão de frequência aplicada à carteira fixa de todos os vendedores da empresa. Clientes inativos são separados pelo CNAE do ERP: os que começam com 03, 47 ou 27 são atendidos a cada 30 dias e os demais a cada 15 dias. Clientes ativos e clientes sem venda são atendidos a cada 30 dias. A última regra para inativos nunca é aplicada, pois esses clientes já são tratados pelas regras anteriores.

## Carteiras

| Carteira | Descrição |
|---|---|
| empresa toda | Carteira fixa de todos os vendedores da empresa |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos com CNAE 03, 47 ou 27 | Clientes inativos para o vendedor com CNAE do ERP começando com 03, 47 ou 27 | 30 dias | Preferência de dias configurada pelo vendedor |
| Inativos com outros CNAEs | Clientes inativos para o vendedor com CNAE do ERP que não começa com 03, 47 nem 27 | 15 dias | Preferência de dias configurada pelo vendedor |
| Ativos | Clientes ativos para o vendedor | 30 dias | Preferência de dias configurada pelo vendedor |
| Inativos | Clientes inativos para o vendedor | 15 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Sem vendas | Clientes sem vendas para o vendedor | 30 dias | Preferência de dias configurada pelo vendedor |

## Pontos de atenção

- A regra '15 dias para inativos' (R4) nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
