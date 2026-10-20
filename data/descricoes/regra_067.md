# regra_067.gobr

Regras padrão de frequência para três grupos: o time de televendas, a carteira fixa do time capital e o time interior, por situação do cliente e, em capital e interior, por adimplência. Atendimento de segunda a sexta. Inativos inadimplentes da capital não são agendados, e a regra de bloqueio do interior nunca é aplicada. O interior atende inativos inadimplentes a cada 42 dias.

## Carteiras

| Carteira | Descrição |
|---|---|
| capital | Carteira fixa dos vendedores do time capital |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos (televendas) | Clientes ativos para o vendedor, do time televendas | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos (televendas) | Clientes inativos para o vendedor, do time televendas | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor, do time televendas | 7 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Ativos adimplentes (capital) | Clientes adimplentes e ativos para o vendedor, na carteira capital | 20 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Ativos inadimplentes (capital) | Clientes inadimplentes e ativos para o vendedor, na carteira capital | 20 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes (capital) | Clientes adimplentes e inativos para o vendedor, na carteira capital | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (capital) | Clientes inadimplentes e inativos para o vendedor, na carteira capital | Não agendar |  |
| Sem vendas (capital) | Clientes que nunca compraram com o vendedor, na carteira capital | 30 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Ativos (interior) | Clientes ativos para o vendedor, do time interior | 21 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos adimplentes (interior) | Clientes adimplentes e inativos para o vendedor, do time interior | 21 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Inativos inadimplentes (interior) | Clientes inadimplentes e inativos para o vendedor, do time interior | 42 dias | Preferência de segunda a sexta; demais dias sem atendimento |
| Bloqueio: inativos inadimplentes (interior) | Clientes inadimplentes e inativos para o vendedor, na carteira capital, exceto os já tratados pelas regras anteriores | Não agendar | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Sem vendas (interior) | Clientes que nunca compraram com o vendedor, do time interior | 14 dias | Preferência de segunda a sexta; demais dias sem atendimento |

## Pontos de atenção

- O nome da regra '30 dias para clientes inativos inadimplentes (capital)' fala em 30 dias, mas a regra usa outro valor.
- O nome da regra '14 dias para clientes sem venda (capital)' fala em 14 dias, mas a regra usa outro valor.
- A regra 'clientes inativos inadimplentes (interior)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
