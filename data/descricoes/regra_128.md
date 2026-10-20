# regra_128.gobr

Regra de agendamento de seis times de televendas (tmk_1, tmk_2, tmk_3, tmk_5, tmk_6 e tmk_7), cada um com faixas próprias para a carteira de um par de equipes externas: prospects, ativos, retenção e recuperação. Prospects, retenção e recuperação seguem frequência de 7 dias; os ativos das equipes externas, de 5 dias, somente a partir do dia 16 de cada mês. Depois dessas faixas vêm as regras exclusivas do televendas. Clientes baixados na Receita Federal não são agendados, e quem não se enquadra em nenhuma regra também não.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects Tmk 1 (Niteroi e Rio 2) | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos Tmk 1 (Niteroi e Rio 2) | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção Tmk 1 (Niteroi e Rio 2) | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias | 7 dias |  |
| Recuperação Tmk 1 (Niteroi e Rio 2) | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Prospects Tmk 2 (Lagos e Norte) | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos Tmk 2 (Lagos e Norte) | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção Tmk 2 (Lagos e Norte) | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias | 7 dias |  |
| Recuperação Tmk 2 (Lagos e Norte) | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Prospects Tmk 3 (Baixada 1 e 3) | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos Tmk 3 (Baixada 1 e 3) | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção Tmk 3 (Baixada 1 e 3) | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias | 7 dias |  |
| Recuperação Tmk 3 (Baixada 1 e 3) | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Prospects Tmk 5 (Rio 1 e 3) | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos Tmk 5 (Rio 1 e 3) | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção Tmk 5 (Rio 1 e 3) | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias | 7 dias |  |
| Recuperação Tmk 5 (Rio 1 e 3) | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Prospects Tmk 6 (Sul Flu 1 e 2) | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos Tmk 6 (Sul Flu 1 e 2) | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção Tmk 6 (Sul Flu 1 e 2) | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias | 7 dias |  |
| Recuperação Tmk 6 (Sul Flu 1 e 2) | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Prospects Tmk 7 (Serrana e Baixada 2) | Clientes que nunca compraram com qualquer vendedor da empresa | 7 dias |  |
| Ativos Tmk 7 (Serrana e Baixada 2) | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção Tmk 7 (Serrana e Baixada 2) | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias | 7 dias |  |
| Recuperação Tmk 7 (Serrana e Baixada 2) | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias |  |
| Prospects exclusivos do televendas | Clientes que nunca compraram com qualquer vendedor da empresa, exceto os já tratados pelas regras anteriores | 7 dias | Vale para os seis times tmk |
| Ativos exclusivos do televendas | Clientes que compraram com qualquer vendedor da empresa nos últimos 60 dias, exceto os já tratados pelas regras anteriores | 7 dias | Vale para os seis times tmk |
| Retenção exclusiva do televendas | Clientes que compraram com qualquer vendedor da empresa nos últimos 90 dias, exceto os já tratados pelas regras anteriores | 7 dias | Vale para os seis times tmk |
| Recuperação exclusiva do televendas | Clientes que estão há mais de 90 dias sem comprar com qualquer vendedor da empresa | 7 dias | Vale para os seis times tmk |
| Bloqueio: demais clientes | Todos os clientes dos seis times tmk, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das regras anteriores |

## Pontos de atenção

- O nome da regra 'Ativos / Tmk 1 (Niteroi e Rio 2)' fala em 20 dias, mas a regra usa outro valor: ela é executada a partir do dia 16 de cada mês.
- Nos dias em que 'Ativos / Tmk 1 (Niteroi e Rio 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Tmk 1 (Niteroi e Rio 2)'.
- Nos dias em que 'Ativos / Tmk 1 (Niteroi e Rio 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Recuperação / Tmk 1 (Niteroi e Rio 2)'.
- O nome da regra 'Ativos / Tmk 2 (Lagos e Norte)' fala em 20 dias, mas a regra usa outro valor: ela é executada a partir do dia 16 de cada mês.
- Nos dias em que 'Ativos / Tmk 2 (Lagos e Norte)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Tmk 2 (Lagos e Norte)'.
- Nos dias em que 'Ativos / Tmk 2 (Lagos e Norte)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Recuperação / Tmk 2 (Lagos e Norte)'.
- O nome da regra 'Ativos / Tmk 3 (Baixada 1 e 3)' fala em 20 dias, mas a regra usa outro valor: ela é executada a partir do dia 16 de cada mês.
- Nos dias em que 'Ativos / Tmk 3 (Baixada 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Tmk 3 (Baixada 1 e 3)'.
- Nos dias em que 'Ativos / Tmk 3 (Baixada 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Recuperação / Tmk 3 (Baixada 1 e 3)'.
- O nome da regra 'Ativos / Tmk 5 (Rio 1 e 3)' fala em 20 dias, mas a regra usa outro valor: ela é executada a partir do dia 16 de cada mês.
- Nos dias em que 'Ativos / Tmk 5 (Rio 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Tmk 5 (Rio 1 e 3)'.
- Nos dias em que 'Ativos / Tmk 5 (Rio 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Recuperação / Tmk 5 (Rio 1 e 3)'.
- O nome da regra 'Ativos / Tmk 6 (Sul Flu 1 e 2)' fala em 20 dias, mas a regra usa outro valor: ela é executada a partir do dia 16 de cada mês.
- Nos dias em que 'Ativos / Tmk 6 (Sul Flu 1 e 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Tmk 6 (Sul Flu 1 e 2)'.
- Nos dias em que 'Ativos / Tmk 6 (Sul Flu 1 e 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Recuperação / Tmk 6 (Sul Flu 1 e 2)'.
- O nome da regra 'Ativos / Tmk 7 (Serrana e Baixada 2)' fala em 20 dias, mas a regra usa outro valor: ela é executada a partir do dia 16 de cada mês.
- Nos dias em que 'Ativos / Tmk 7 (Serrana e Baixada 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Tmk 7 (Serrana e Baixada 2)'.
- Nos dias em que 'Ativos / Tmk 7 (Serrana e Baixada 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Recuperação / Tmk 7 (Serrana e Baixada 2)'.
- A condição da regra 'Prospects / Exclusivo do televendas' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- Nos dias em que 'Ativos / Tmk 1 (Niteroi e Rio 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Ativos / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 2 (Lagos e Norte)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Ativos / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 3 (Baixada 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Ativos / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 5 (Rio 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Ativos / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 6 (Sul Flu 1 e 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Ativos / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 7 (Serrana e Baixada 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Ativos / Exclusivo do televendas'.
- A condição da regra 'Ativos / Exclusivo do televendas' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- Nos dias em que 'Ativos / Tmk 1 (Niteroi e Rio 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 2 (Lagos e Norte)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 3 (Baixada 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 5 (Rio 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 6 (Sul Flu 1 e 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Exclusivo do televendas'.
- Nos dias em que 'Ativos / Tmk 7 (Serrana e Baixada 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes de 'Retenção / Exclusivo do televendas'.
- A condição da regra 'Retenção / Exclusivo do televendas' é fragmentada demais para resumir: ela vale para os clientes da condição própria, exceto os já tratados pelas regras anteriores.
- Nos dias em que 'Ativos / Tmk 1 (Niteroi e Rio 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes da regra final 'Clientes que hoje não se enquadraram'.
- Nos dias em que 'Ativos / Tmk 2 (Lagos e Norte)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes da regra final 'Clientes que hoje não se enquadraram'.
- Nos dias em que 'Ativos / Tmk 3 (Baixada 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes da regra final 'Clientes que hoje não se enquadraram'.
- Nos dias em que 'Ativos / Tmk 5 (Rio 1 e 3)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes da regra final 'Clientes que hoje não se enquadraram'.
- Nos dias em que 'Ativos / Tmk 6 (Sul Flu 1 e 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes da regra final 'Clientes que hoje não se enquadraram'.
- Nos dias em que 'Ativos / Tmk 7 (Serrana e Baixada 2)' é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes da regra final 'Clientes que hoje não se enquadraram'.
- A condição da regra 'Clientes que hoje não se enquadraram' é fragmentada demais para resumir: ela vale para todos os clientes dos times, exceto os já tratados pelas regras anteriores.
