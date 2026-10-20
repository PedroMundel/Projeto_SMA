# regra_120.gobr

Parametrização por times e carteiras: televendas, capital e interior, com frequência definida pela situação do cliente para o vendedor (ativos, inativos e sem venda) e, em capital e interior, também pela adimplência. Os clientes do time Yasmim (vendedor de id 12) não são agendados. Há ainda bloqueios para inativos inadimplentes da capital e do interior, mas o do interior nunca é aplicado. As regras de frequência atendem de segunda a sexta.

## Carteiras

| Carteira | Descrição |
|---|---|
| televendas | Carteira fixa dos vendedores do time televendas |
| interior | Carteira fixa dos vendedores do time interior |
| capital | Carteira fixa dos vendedores do time capital |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: time Yasmim | Clientes de todos os tipos atendidos pelo time Yasmim (vendedor de id 12) | Não agendar |  |
| Televendas: ativos | Clientes ativos para o vendedor, na carteira televendas | 14 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Televendas: inativos | Clientes inativos para o vendedor, na carteira televendas | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Televendas: sem venda | Clientes sem vendas para o vendedor, na carteira televendas | 7 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Capital: ativos adimplentes | Clientes adimplentes e ativos para o vendedor, na carteira capital | 20 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Capital: ativos inadimplentes | Clientes inadimplentes e ativos para o vendedor, na carteira capital | 20 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Capital: inativos adimplentes | Clientes adimplentes e inativos para o vendedor, na carteira capital | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Capital: sem venda | Clientes sem vendas para o vendedor, na carteira capital | 30 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (capital) | Clientes inadimplentes e inativos para o vendedor, na carteira capital | Não agendar |  |
| Interior: ativos | Clientes ativos para o vendedor, na carteira interior | 21 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Interior: inativos adimplentes | Clientes adimplentes e inativos para o vendedor, na carteira interior | 21 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Interior: inativos inadimplentes | Clientes inadimplentes e inativos para o vendedor, na carteira interior | 42 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Interior: sem venda | Clientes sem vendas para o vendedor, na carteira interior | 38 dias | Dias de preferência: segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (interior) | Clientes inadimplentes e inativos para o vendedor, na carteira interior | Não agendar | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- O nome da regra 'Capital: sem venda' fala em 14 dias, mas a regra usa outro valor (30 dias).
- O nome da regra 'Capital: inativos inadimplentes' fala em 30 dias, mas a regra usa outro valor.
- O nome da regra 'Interior: inativos inadimplentes' fala em 30 dias, mas a regra usa outro valor (42 dias).
- A regra 'Bloqueio: inativos inadimplentes (interior)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- O bloqueio 'inativos inadimplentes (interior)' vem depois das faixas de frequência, então não bloqueia clientes que já entraram na regra 'Interior: inativos inadimplentes'.
