# regra_171.gobr

Regra de agendamento do time de televendas por tempo desde a última compra e frequência histórica de compra, em sete faixas (prospects, ativados, ativos de alta frequência, ativos regulares, ativos a estimular, em ruptura e inativos). Antes das faixas, deixam de ser agendados os clientes inadimplentes, os bloqueados para atendimento, as filiais e os baixados na Receita Federal. A última faixa recebe os clientes que sobraram das anteriores e tem frequência de 21 dias.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: bloqueados | Clientes bloqueados para atendimento | Não agendar |  |
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospect: cliente potencial | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Ativado: um pedido só | Clientes que já compraram com qualquer vendedor da empresa, cadastrados no ERP há pelo menos 30 dias e com uma única compra na empresa | 10 dias |  |
| Ativo: alta frequência de compra | Clientes que compraram nos últimos 30 dias e têm frequência histórica de compra de menos de 14 dias | 14 dias | Compra única só entra se o cliente foi cadastrado no ERP há menos de 30 dias |
| Ativo: compra regularmente | Clientes que compraram nos últimos 30 dias e têm frequência histórica de compra entre 14 e 29 dias | Pelo histórico, entre 14 e 28 dias | Compra única só entra se o cliente foi cadastrado no ERP há menos de 30 dias |
| Ativo: estimular regularidade | Clientes que compraram nos últimos 60 dias, mas estão há pelo menos 21 dias sem comprar, exceto os já tratados pelas regras anteriores | 14 dias |  |
| Em ruptura: risco de inatividade | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 7 dias | Compra única só entra se o cliente foi cadastrado no ERP há menos de 30 dias |
| Inativos: reativar | Clientes que compraram nos últimos 89 dias ou estão há mais de 180 dias sem comprar, exceto os já tratados pelas regras anteriores | 21 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- O nome da regra 'Freq. de 21d para 'Ativo: compra regularmente'' fala em 21 dias, mas a regra usa outro valor (frequência pelo histórico, entre 14 e 28 dias).
- Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar, e não são de compra única (ou são de compra única cadastrados no ERP há menos de 30 dias) não se enquadram em nenhuma regra e ficam sem parametrização.
