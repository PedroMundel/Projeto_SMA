# regra_143.gobr

Regra de agendamento do time de televendas por tempo sem comprar, ciclo de vida e curva de clientes. Não são agendadas as filiais e os clientes que compraram com a empresa nos últimos 30 dias. Prospects têm frequência de 28 dias; ativos com mais de 45 dias sem comprar são divididos por curva A, B e demais, há faixas para ativos com compra recente e uma faixa final para inativos.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram com qualquer vendedor da empresa nos últimos 30 dias | Não agendar |  |
| Prospects | Clientes que nunca compraram com a empresa | 28 dias |  |
| Ativos sem compra (Curva A) | Clientes ativos na empresa, curva A, que estão há mais de 45 dias sem comprar com a empresa | 7 dias |  |
| Ativos sem compra (Curva B) | Clientes ativos na empresa, curva B, que estão há mais de 45 dias sem comprar com a empresa | 14 dias |  |
| Ativos sem compra (Curva C) | Clientes ativos na empresa, fora das curvas A e B, que estão há mais de 45 dias sem comprar com a empresa | 21 dias |  |
| Ativos sem compra (até 44 dias) | Clientes ativos na empresa que compraram nos últimos 44 dias, mas estão há mais de 30 dias sem comprar | 14 dias |  |
| Ativos sem compra (45 dias) | Clientes ativos na empresa que compraram nos últimos 45 dias, mas estão há pelo menos 45 dias sem comprar | 7 dias |  |
| Inativos | Clientes fora do ciclo de vida ativo na empresa que estão há mais de 30 dias sem comprar com a empresa | 7 dias | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- O nome da regra 'Ativos sem compra com a empresa há mais de 60d' fala em 60 dias, mas a regra usa outro valor.
