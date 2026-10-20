# regra_154.gobr

Regra de agendamento do time de todos os vendedores de televendas, organizada primeiro por cidade e depois por perfil de compra. Nove rotas por cidade têm frequência semanal de 7 dias, quatro delas fixas por dia da semana e cinco dinâmicas. Para as demais cidades, as faixas são prospects, ativos por curva A, B e C, e inativos.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Rota fixa de segunda | Clientes das cidades BALNEARIO BARRA DO S, BELA VISTA, CAMPO ALEGRE, CANOINHAS, CORUPA, ITAIOPOLIS e mais 8 | 7 dias | Fixo, restrição rígida de frequência e dias; preferência segunda, demais dias sem atendimento |
| Rota fixa de terça | Clientes das cidades APIUNA, ASCURRA, BENEDITO NOVO, BLUMENAU, DOUTOR PEDRINHO, GASPAR e mais 6 | 7 dias | Fixo, restrição rígida de frequência e dias; preferência terça, demais dias sem atendimento |
| Rota fixa de quarta | Clientes das cidades ARARANGUA, BIGUACU, BRACO DO NORTE, CAPIVARI DE BAIXO, COCAL DO SUL, CRICIUMA e mais 23 | 7 dias | Fixo, restrição rígida de frequência e dias; preferência quarta, demais dias sem atendimento |
| Rota fixa de quinta | Clientes das cidades ARAQUARI, MASSARANDUBA, PIRABEIRABA e SAO JOAO DO ITAPERIU | 7 dias | Fixo, restrição rígida de frequência e dias; preferência quinta, demais dias sem atendimento |
| Rota dinâmica segunda, terça ou sexta | Clientes da cidade de BRUSQUE | 7 dias | Preferência segunda, terça e sexta; demais dias sem atendimento |
| Rota dinâmica terça ou sexta | Clientes da cidade de NOVA TRENTO | 7 dias | Preferência terça e sexta; demais dias sem atendimento |
| Rota dinâmica segunda ou quinta | Clientes das cidades GUARAMIRIM, JARAGUA DO SUL, JOINVILLE e SCHROEDER | 7 dias | Preferência segunda e quinta; demais dias sem atendimento |
| Rota dinâmica terça ou quinta | Clientes das cidades BALNEARIO PICARRAS, BARRA VELHA, NAVEGANTES e PENHA | 7 dias | Preferência terça e quinta; demais dias sem atendimento |
| Rota dinâmica de dias variados | Clientes das cidades BALNEARIO CAMBORIU, CAMBORIU, CANELINHA, ITAJAI, ITAPEMA, PORTO BELO e mais 2 | 7 dias | Sem dias de preferência definidos |
| Prospects | Clientes que nunca compraram na empresa, fora das cidades das rotas anteriores | 30 dias |  |
| Ativos - Curva A | Clientes ativos para o vendedor, curva A na empresa, fora das cidades das rotas anteriores | 14 dias |  |
| Ativos - Curva B | Clientes ativos para o vendedor, curva B na empresa, fora das cidades das rotas anteriores | 21 dias |  |
| Ativos - Curva C | Clientes ativos para o vendedor, fora das curvas A e B na empresa, fora das cidades das rotas anteriores | 28 dias |  |
| Inativos | Clientes que já compraram na empresa e não são ativos para o vendedor, fora das cidades das rotas anteriores | 30 dias |  |
