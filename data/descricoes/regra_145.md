# regra_145.gobr

Regra de agendamento aplicada a todos os vendedores da empresa, com faixas de frequência por tempo desde a última compra com o vendedor: ativação de prospects, compra regular, estímulo à regularidade, risco de inatividade e resgate. Só clientes pessoa jurídica entram nas faixas, e as filiais não são agendadas. A regra final de resgate cobre inadimplentes que já compraram e adimplentes sem compra há mais de 90 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Ativação de prospects | Clientes pessoa jurídica que nunca compraram com o próprio vendedor | 10 dias |  |
| Primeira compra (Indústria) | Clientes pessoa jurídica do ramo de atividade 2 sem vendas para o vendedor | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Primeira compra (Revenda) | Clientes pessoa jurídica do ramo de atividade 1 sem vendas para o vendedor | 7 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Estimular a regularidade de compra | Clientes pessoa jurídica adimplentes que compraram com o próprio vendedor nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 14 dias |  |
| Compra regularmente | Clientes pessoa jurídica adimplentes que compraram com o próprio vendedor nos últimos 30 dias | 21 dias |  |
| Risco de inatividade | Clientes pessoa jurídica adimplentes que compraram com o próprio vendedor nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias |  |
| Resgate de clientes sem compra | Clientes pessoa jurídica que já compraram com o vendedor e estão inadimplentes, ou adimplentes há mais de 90 dias sem comprar com ele | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A regra 'Freq. de 14d para Primeira compra (Indústria)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'Freq. de 7d para Primeira compra (Revenda)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- Clientes que são pessoa física ou sem tipo de pessoa definido não se enquadram em nenhuma regra e ficam sem parametrização.
