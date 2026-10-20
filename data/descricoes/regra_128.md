# regra_128.gobr

Regra de agendamento de seis times de televendas (Tmk 1, 2, 3, 5, 6 e 7), cada um recebendo por segmentação a carteira fixa de um par de times externos. Em cada segmentação as faixas são prospects, ativos (últimos 60 dias, aplicada somente a partir do dia 16 de cada mês), retenção (últimos 90 dias) e recuperação (mais de 90 dias sem comprar); as mesmas faixas valem depois para os clientes exclusivos do televendas. Clientes baixados na Receita Federal não são agendados, e a regra final também não agenda quem não se enquadrou em nenhuma faixa.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Prospects - Niterói e Rio 2 (Tmk 1) | Clientes que nunca compraram na empresa e estão na segmentação ext_niteroi_rio2_para_tmk1 | 7 dias |  |
| Ativos - Niterói e Rio 2 (Tmk 1) | Clientes que compraram na empresa nos últimos 60 dias e estão na segmentação ext_niteroi_rio2_para_tmk1 | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção - Niterói e Rio 2 (Tmk 1) | Clientes que compraram na empresa nos últimos 90 dias e estão na segmentação ext_niteroi_rio2_para_tmk1 | 7 dias |  |
| Recuperação - Niterói e Rio 2 (Tmk 1) | Clientes que estão há mais de 90 dias sem comprar na empresa e estão na segmentação ext_niteroi_rio2_para_tmk1 | 7 dias |  |
| Prospects - Lagos e Norte (Tmk 2) | Clientes que nunca compraram na empresa e estão na segmentação ext_lagos_norte_para_tmk2 | 7 dias |  |
| Ativos - Lagos e Norte (Tmk 2) | Clientes que compraram na empresa nos últimos 60 dias e estão na segmentação ext_lagos_norte_para_tmk2 | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção - Lagos e Norte (Tmk 2) | Clientes que compraram na empresa nos últimos 90 dias e estão na segmentação ext_lagos_norte_para_tmk2 | 7 dias |  |
| Recuperação - Lagos e Norte (Tmk 2) | Clientes que estão há mais de 90 dias sem comprar na empresa e estão na segmentação ext_lagos_norte_para_tmk2 | 7 dias |  |
| Prospects - Baixada 1 e 3 (Tmk 3) | Clientes que nunca compraram na empresa e estão na segmentação ext_baixada1_baixada3_para_tmk3 | 7 dias |  |
| Ativos - Baixada 1 e 3 (Tmk 3) | Clientes que compraram na empresa nos últimos 60 dias e estão na segmentação ext_baixada1_baixada3_para_tmk3 | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção - Baixada 1 e 3 (Tmk 3) | Clientes que compraram na empresa nos últimos 90 dias e estão na segmentação ext_baixada1_baixada3_para_tmk3 | 7 dias |  |
| Recuperação - Baixada 1 e 3 (Tmk 3) | Clientes que estão há mais de 90 dias sem comprar na empresa e estão na segmentação ext_baixada1_baixada3_para_tmk3 | 7 dias |  |
| Prospects - Rio 1 e 3 (Tmk 5) | Clientes que nunca compraram na empresa e estão na segmentação ext_rio1_rio3_para_tmk5 | 7 dias |  |
| Ativos - Rio 1 e 3 (Tmk 5) | Clientes que compraram na empresa nos últimos 60 dias e estão na segmentação ext_rio1_rio3_para_tmk5 | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção - Rio 1 e 3 (Tmk 5) | Clientes que compraram na empresa nos últimos 90 dias e estão na segmentação ext_rio1_rio3_para_tmk5 | 7 dias |  |
| Recuperação - Rio 1 e 3 (Tmk 5) | Clientes que estão há mais de 90 dias sem comprar na empresa e estão na segmentação ext_rio1_rio3_para_tmk5 | 7 dias |  |
| Prospects - Sul Flu 1 e 2 (Tmk 6) | Clientes que nunca compraram na empresa e estão na segmentação ext_sulflu1_sulflu2_para_tmk6 | 7 dias |  |
| Ativos - Sul Flu 1 e 2 (Tmk 6) | Clientes que compraram na empresa nos últimos 60 dias e estão na segmentação ext_sulflu1_sulflu2_para_tmk6 | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção - Sul Flu 1 e 2 (Tmk 6) | Clientes que compraram na empresa nos últimos 90 dias e estão na segmentação ext_sulflu1_sulflu2_para_tmk6 | 7 dias |  |
| Recuperação - Sul Flu 1 e 2 (Tmk 6) | Clientes que estão há mais de 90 dias sem comprar na empresa e estão na segmentação ext_sulflu1_sulflu2_para_tmk6 | 7 dias |  |
| Prospects - Serrana e Baixada 2 (Tmk 7) | Clientes que nunca compraram na empresa e estão na segmentação ext_serrana_baixada2_para_tmk7 | 7 dias |  |
| Ativos - Serrana e Baixada 2 (Tmk 7) | Clientes que compraram na empresa nos últimos 60 dias e estão na segmentação ext_serrana_baixada2_para_tmk7 | 5 dias | Executada somente a partir do dia 16 de cada mês |
| Retenção - Serrana e Baixada 2 (Tmk 7) | Clientes que compraram na empresa nos últimos 90 dias e estão na segmentação ext_serrana_baixada2_para_tmk7 | 7 dias |  |
| Recuperação - Serrana e Baixada 2 (Tmk 7) | Clientes que estão há mais de 90 dias sem comprar na empresa e estão na segmentação ext_serrana_baixada2_para_tmk7 | 7 dias |  |
| Prospects - Exclusivo do televendas | Clientes que nunca compraram na empresa, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Ativos - Exclusivo do televendas | Clientes que compraram na empresa nos últimos 60 dias, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Retenção - Exclusivo do televendas | Clientes que compraram na empresa nos últimos 90 dias, exceto os já tratados pelas regras anteriores | 7 dias |  |
| Recuperação - Exclusivo do televendas | Clientes que estão há mais de 90 dias sem comprar na empresa e fora das seis segmentações de externos para o televendas | 7 dias |  |
| Demais clientes | Clientes dos times de televendas, exceto os já tratados pelas regras anteriores | Não agendar | Regra final: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- O nome da regra 'Ativos (A partir do dia 20 de cada mês)' do Tmk 1 fala em 20 dias, mas a regra só é executada a partir do dia 16 de cada mês.
- O nome da regra 'Ativos (A partir do dia 20 de cada mês)' do Tmk 2 fala em 20 dias, mas a regra só é executada a partir do dia 16 de cada mês.
- O nome da regra 'Ativos (A partir do dia 20 de cada mês)' do Tmk 3 fala em 20 dias, mas a regra só é executada a partir do dia 16 de cada mês.
- O nome da regra 'Ativos (A partir do dia 20 de cada mês)' do Tmk 5 fala em 20 dias, mas a regra só é executada a partir do dia 16 de cada mês.
- O nome da regra 'Ativos (A partir do dia 20 de cada mês)' do Tmk 6 fala em 20 dias, mas a regra só é executada a partir do dia 16 de cada mês.
- O nome da regra 'Ativos (A partir do dia 20 de cada mês)' do Tmk 7 fala em 20 dias, mas a regra só é executada a partir do dia 16 de cada mês.
- Nos dias em que a regra 'Ativos' do Tmk 1 é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes das regras de retenção, recuperação, exclusivas do televendas e final.
- Nos dias em que a regra 'Ativos' do Tmk 2 é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes das regras de retenção, recuperação, exclusivas do televendas e final.
- Nos dias em que a regra 'Ativos' do Tmk 3 é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes das regras de retenção, recuperação, exclusivas do televendas e final.
- Nos dias em que a regra 'Ativos' do Tmk 5 é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes das regras de retenção, recuperação, exclusivas do televendas e final.
- Nos dias em que a regra 'Ativos' do Tmk 6 é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes das regras de retenção, recuperação, exclusivas do televendas e final.
- Nos dias em que a regra 'Ativos' do Tmk 7 é executada (a partir do dia 16 de cada mês), os clientes dela são tratados por ela antes das regras de retenção, recuperação, exclusivas do televendas e final.
