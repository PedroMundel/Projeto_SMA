# regra_145.gobr

Regra de agendamento do time da empresa toda, voltada a clientes pessoa jurídica, organizada por tempo desde a última compra com o próprio vendedor. Há faixas para prospects, primeira compra (indústria e revenda), regularidade de compra, compra regular e risco de inatividade, e uma regra final de resgate. As filiais não são agendadas.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativação de prospects | Clientes pessoa jurídica que nunca compraram com o próprio vendedor | 10 dias |  |
| Primeira compra (Indústria) | Clientes pessoa jurídica do ramo de atividade (id) 2 que já compraram com o próprio vendedor e estão sem vendas para o vendedor | 14 dias |  |
| Primeira compra (Revenda) | Clientes pessoa jurídica do ramo de atividade (id) 1 que já compraram com o próprio vendedor e estão sem vendas para o vendedor | 7 dias |  |
| Estimular a regularidade de compra | Clientes pessoa jurídica adimplentes que compraram com o próprio vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias |  |
| Compra regularmente | Clientes pessoa jurídica adimplentes que compraram com o próprio vendedor nos últimos 30 dias | 21 dias |  |
| Risco de inatividade | Clientes pessoa jurídica adimplentes que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Resgate de clientes sem compra | Clientes pessoa jurídica, exceto os já tratados pelas regras anteriores | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A condição da regra 'Resgate de clientes sem compra' é fragmentada demais para resumir: ela vale para pessoas jurídicas, exceto os clientes já tratados pelas regras anteriores.
- Clientes pessoa física não se enquadram em nenhuma regra e ficam sem parametrização.
