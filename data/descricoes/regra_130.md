# regra_130.gobr

Regra padrão com parametrização separada para o time interno (televendas) e para o time externo (campo). No televendas, deixam de ser agendados os clientes pessoa física, os inativos inadimplentes e os pessoa física sem compra; pessoas jurídicas são atendidas a cada 7, 15 ou 20 dias conforme estejam ativas, inativas adimplentes ou sem vendas. No campo, ativos têm frequência de 7 dias e os demais de 15 dias, com parametrização fixa.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: pessoa física (Televendas) | Clientes pessoa física | Não agendar |  |
| Ativos (Televendas) | Clientes pessoa jurídica ativos para o vendedor | 7 dias |  |
| Inativos adimplentes (Televendas) | Clientes pessoa jurídica adimplentes e inativos para o vendedor | 15 dias |  |
| Bloqueio: inativos inadimplentes (Televendas) | Clientes pessoa jurídica inadimplentes e inativos para o vendedor | Não agendar |  |
| Bloqueio: sem compra e pessoa física (Televendas) | Clientes pessoa física sem vendas para o vendedor | Não agendar | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Sem compra e CNPJ (Televendas) | Clientes pessoa jurídica sem vendas para o vendedor | 20 dias |  |
| Ativos (campo) | Clientes ativos para o vendedor | 7 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |
| Inativos (campo) | Clientes que não estão ativos para o vendedor | 15 dias | Parametrização fixa: restrição rígida de frequência e dias para o gerador de agendas |

## Pontos de atenção

- A regra 'Não agendar clientes sem compra e CPF (Televendas)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores ('Não agendar clientes CPF (Televendas)').
- O nome da regra 'Frequencia de 14 dias para clientes inativos (campo)' fala em 14 dias, mas a regra usa outro valor (15 dias).
