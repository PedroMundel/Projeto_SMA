# regra_183.gobr

Regra de agendamento do time de televendas por perfil de compra do cliente. Inadimplentes não são agendados. Prospects têm frequência de 21 dias; quem já comprou segue a frequência pelo histórico de compras ou frequências de 14 e 21 dias, conforme a frequência histórica e a situação de ativo ou inativo. Uma das faixas nunca é aplicada e há clientes sem nenhuma regra.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 21 dias |  |
| Alta frequência de compra | Clientes que já compraram na empresa, ativos para o vendedor e com frequência histórica de compra de menos de 30 dias | Pelo histórico, entre 5 e 30 dias |  |
| Compra regularmente (sem pedido em 30d) | Clientes que já compraram na empresa, ativos para o vendedor e com frequência histórica de compra de mais de 30 dias | 14 dias |  |
| Compra regularmente (com pedido em 30d) | Clientes que compraram com o próprio vendedor nos últimos 30 dias, com frequência histórica de compra de mais de 30 dias e ativos para o vendedor | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Inativos | Clientes inativos da empresa que já compraram e não são ativos para o vendedor, ou ativos com frequência histórica indefinida ou de 30 dias | 21 dias |  |

## Pontos de atenção

- A regra 'Freq. de 14d para Compra regularmente (Com pedido em 30d)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- Clientes que já compraram, estão fora do ciclo de vida inativo com a empresa e não são ativos para o vendedor, ou são ativos com frequência histórica indefinida ou de 30 dias, não se enquadram em nenhuma regra e ficam sem parametrização.
