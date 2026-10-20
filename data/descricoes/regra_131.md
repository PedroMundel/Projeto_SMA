# regra_131.gobr

Regras de agendamento para os times de televendas e de campo, organizadas por CNAE, crédito disponível e situação de ativo ou inativo para o vendedor. Antes das frequências, deixam de ser agendados os clientes inadimplentes e os com CNAE de administração pública em geral e segurança e ordem pública. Clientes sem crédito disponível têm frequência de 7 dias nos dois times. Com crédito, há três modelos por CNAE (ativos e inativos nos modelos 1 e 2, e um modelo único para os demais), e o time de campo atende apenas em dias de preferência.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar | Vale para os times televendas e campo |
| Bloqueio: administração e segurança pública | Clientes com CNAE (id) em 8411600 ou 8424800 | Não agendar | Vale para os times televendas e campo |
| Sem crédito | Clientes com CNAE fora de 8411600 e 8424800 e sem crédito disponível | 7 dias | Vale para os times televendas e campo |
| Modelo 1 - ativos (televendas) | Clientes com CNAE (id) em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e ativos para o vendedor | 7 dias |  |
| Modelo 1 - inativos (televendas) | Clientes com CNAE (id) em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e não ativos para o vendedor | 14 dias |  |
| Modelo 2 - ativos (televendas) | Clientes com CNAE (id) em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e ativos para o vendedor | 21 dias |  |
| Modelo 2 - inativos (televendas) | Clientes com CNAE (id) em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e não ativos para o vendedor | 30 dias |  |
| Modelo 3 (televendas) | Clientes com CNAE (id) fora de 3250705, 4645101, 4773300, 7500100, 8411600, 8424800 e mais 9, com crédito disponível | 30 dias |  |
| Modelo 1 - ativos (externos) | Clientes com CNAE (id) em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e ativos para o vendedor | 7 dias | Preferência: segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 1 - inativos (externos) | Clientes com CNAE (id) em 7500100, 8610101, 8610102, 8630501, 8630502, 8630503 e mais 2, com crédito disponível e não ativos para o vendedor | 14 dias | Preferência: segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 2 - ativos (externos) | Clientes com CNAE (id) em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e ativos para o vendedor | 21 dias | Preferência: segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 2 - inativos (externos) | Clientes com CNAE (id) em 3250705, 4645101, 4773300, 8532500, 8533300, com crédito disponível e não ativos para o vendedor | 30 dias | Preferência: segunda, quarta e sexta; demais dias sem atendimento |
| Modelo 3 (externos) | Clientes com CNAE (id) fora de 3250705, 4645101, 4773300, 7500100, 8411600, 8424800 e mais 9, com crédito disponível | 30 dias | Preferência: segunda, quarta e sexta; demais dias sem atendimento |
