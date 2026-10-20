# regra_236.gobr

Regra de agendamento do time de televendas organizada em sete carteiras fixas por UF, cidade e bairro, com rotas todos os dias, às segundas, quartas e sextas, e às terças e quintas. Nas carteiras de rota diária a frequência é de 7 dias para quem comprou recentemente e de 2 dias para os demais; nas outras, a frequência é semanal para quem não comprou na semana atual. Não são agendados os baixados na Receita, e a regra final bloqueia quem está fora das carteiras ou já comprou na semana.

## Carteiras

| Carteira | Descrição |
|---|---|
| cidades_todo_dia | Carteira fixa do time televendas: UF RJ e cidades como BARRA MANSA, BELFORD ROXO, ITATIAIA, MESQUITA, NOVA IGUAÇU, PORTO REAL e mais 4 |
| bairros_todo_dia | Carteira fixa do time televendas: UF RJ, cidade RIO DE JANEIRO e bairros como CENTRO e PAVUNA |
| cidades_seg_qua_sex | Carteira fixa do time televendas: UF RJ e cidades ITAGUAI, SEROPEDICA e VISCONDE DE MAUA |
| bairros_seg_qua_sex | Carteira fixa do time televendas: UF RJ, cidade RIO DE JANEIRO e bairros como BANGU, BARRA DA TIJUCA, CACHAMBI, CAMPO GRANDE e mais 69 |
| cidades_rj_ter_qui | Carteira fixa do time televendas: UF RJ e cidades como BANANAL, BARRA DO PIRAI, MANGARATIBA, MENDES, MIGUEL PEREIRA e mais 12 |
| bairros_rj_ter_qui | Carteira fixa do time televendas: UF RJ, cidades ANGRA DOS REIS e RIO DE JANEIRO, e bairros como GUARATIBA e PARQUE PEREQUE e mais 3 |
| cidades_sp_ter_qui | Carteira fixa do time televendas: UF SP e cidade SAO PAULO |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: baixados na Receita | Clientes com situação baixada na Receita Federal | Não agendar |  |
| Rota todo dia, com venda recente | Clientes das carteiras cidades_todo_dia e bairros_todo_dia que compraram no último dia (1 dia) | 7 dias |  |
| Rota todo dia | Clientes das carteiras cidades_todo_dia e bairros_todo_dia que nunca compraram ou estão há mais de 1 dia sem comprar | 2 dias |  |
| Rota segunda, quarta e sexta | Clientes das carteiras cidades_seg_qua_sex e bairros_seg_qua_sex que não compraram na semana atual | 7 dias | Dias de preferência: segunda, quarta, sexta |
| Rota terça e quinta | Clientes das carteiras cidades_rj_ter_qui, bairros_rj_ter_qui e cidades_sp_ter_qui que não compraram na semana atual | 7 dias | Dias de preferência: terça, quinta |
| Demais clientes | Clientes fora das carteiras de rota ou, nas carteiras de segunda, quarta e sexta e de terça e quinta, que já compraram na semana atual | Não agendar | Regra final: vale para quem sobrou das regras anteriores |

## Pontos de atenção

- As carteiras 'cidades_todo_dia' e 'bairros_todo_dia' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_todo_dia' e 'cidades_seg_qua_sex' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_todo_dia' e 'bairros_seg_qua_sex' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_todo_dia' e 'cidades_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_todo_dia' e 'bairros_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_todo_dia' e 'cidades_seg_qua_sex' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_todo_dia' e 'bairros_seg_qua_sex' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_todo_dia' e 'bairros_seg_qua_sex' têm a cidade RIO DE JANEIRO em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_todo_dia' e 'cidades_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_todo_dia' e 'bairros_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_todo_dia' e 'bairros_rj_ter_qui' têm a cidade RIO DE JANEIRO em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_seg_qua_sex' e 'bairros_seg_qua_sex' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_seg_qua_sex' e 'cidades_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_seg_qua_sex' e 'bairros_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_seg_qua_sex' e 'cidades_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_seg_qua_sex' e 'bairros_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'bairros_seg_qua_sex' e 'bairros_rj_ter_qui' têm a cidade RIO DE JANEIRO em comum, então os mesmos clientes aparecem nas duas.
- As carteiras 'cidades_rj_ter_qui' e 'bairros_rj_ter_qui' têm o estado RJ em comum, então os mesmos clientes aparecem nas duas.
