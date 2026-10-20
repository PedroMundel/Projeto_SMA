# regra_131.gobr

Regra de agendamento para os times de televendas e de campo. Não são agendados os inadimplentes e os clientes de dois CNAEs (administração pública em geral e segurança e ordem pública). Clientes sem crédito disponível ficam em 7 dias; os demais seguem três modelos por CNAE, com frequências de 7 e 14, 21 e 30, e 30 dias, e o campo tem dias de preferência.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar | Vale para televendas e campo |
| Bloqueio: administração pública e segurança | Clientes com CNAE em 8411600 ou 8424800 | Não agendar | Vale para televendas e campo |
| Sem crédito | Clientes com CNAE fora de 8411600 e 8424800 e sem crédito disponível | 7 dias | Vale para televendas e campo |
| Modelo 1 ativos (televendas) | Clientes com CNAE em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e ativos para o vendedor | 7 dias |  |
| Modelo 1 inativos (televendas) | Clientes com CNAE em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e não ativos para o vendedor | 14 dias |  |
| Modelo 2 ativos (televendas) | Clientes com CNAE em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e ativos para o vendedor | 21 dias |  |
| Modelo 2 inativos (televendas) | Clientes com CNAE em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e não ativos para o vendedor | 30 dias |  |
| Modelo 3 (televendas) | Clientes com CNAE fora de 3250705, 4645101, 4773300, 7500100, 8411600, 8424800 e mais 9 e com crédito disponível | 30 dias |  |
| Modelo 1 ativos (campo) | Clientes com CNAE em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e ativos para o vendedor | 7 dias | Dias de atendimento: preferência segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 1 inativos (campo) | Clientes com CNAE em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e não ativos para o vendedor | 14 dias | Dias de atendimento: preferência segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 2 ativos (campo) | Clientes com CNAE em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e ativos para o vendedor | 21 dias | Dias de atendimento: preferência segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 2 inativos (campo) | Clientes com CNAE em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e não ativos para o vendedor | 30 dias | Dias de atendimento: preferência segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 3 (campo) | Clientes com CNAE fora de 3250705, 4645101, 4773300, 7500100, 8411600, 8424800 e mais 9 e com crédito disponível | 30 dias | Dias de atendimento: preferência segunda, quarta e sexta; demais dias sem atendimento |
