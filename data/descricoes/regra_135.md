# regra_135.gobr

Regra de agendamento de dois times de televendas. O time televendas_2 atende seis carteiras fixas, cinco por dia da semana (segunda a sexta) e uma irrestrita; o time televendas_1 é organizado por tempo desde a última compra. Cada carteira de dia da semana tem seis regras (prospects e cinco faixas) com frequência de 7 dias e um dia de preferência, enquanto a irrestrita usa frequências de 7, 14, 21 e 30 dias por perfil e curva A, B ou C. Duas regras gerais do televendas_2 cobrem os clientes fora das carteiras, e o televendas_1 termina com a regra dos inativos há mais de 180 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| segunda_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2 com clientes de AGUAS DE SAO PEDRO, AMERICANA, ARARAS, CHARQUEADA, CORDEIROPOLIS, Cordeirópolis e mais 10 cidades |
| terca_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2 com clientes de AMERICO BRASILIENSE, ARARAQUARA, BARRINHA, CRAVINHOS, DESCALVADO, GUARIBA e mais 15 cidades |
| quarta_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2 com clientes de AGUAI, AGUAS DE LINDOIA, AMPARO, ANDRADAS, ARTUR NOGUEIRA, ENGENHEIRO COELHO e mais 17 cidades |
| quinta_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2 com clientes de ALUMINIO, ARACOIABA DA SERRA, BOITUVA, CERQUILHO, COTIA, IBIUNA e mais 15 cidades |
| sexta_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2 com clientes de ATIBAIA, BRAGANCA PAULISTA, CAMPINAS, CAMPO LIMPO PAULISTA, COSMOPOLIS, HORTOLANDIA e mais 9 cidades |
| irrestrito_televendas_2 | Carteira fixa dos vendedores do time televendas_2 com clientes de ARUJA, BARUERI, CAIEIRAS, CAJAMAR, CARAPICUIBA, DIADEMA e mais 19 cidades |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects (segunda) | Clientes da carteira de segunda que nunca compraram com o próprio vendedor | 7 dias | Dia de preferência: sexta; demais dias sem atendimento |
| Alta frequência (segunda) | Clientes da carteira de segunda que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Dia de preferência: sexta; demais dias sem atendimento |
| Regularidade (segunda) | Clientes da carteira de segunda que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Dia de preferência: sexta; demais dias sem atendimento |
| Risco de inatividade (segunda) | Clientes da carteira de segunda que já compraram com o próprio vendedor, mas estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 7 dias | Dia de preferência: sexta; demais dias sem atendimento |
| Inativos (segunda) | Clientes da carteira de segunda que já compraram com o próprio vendedor, compraram na empresa nos últimos 120 dias e estão há mais de 180 dias sem comprar no grupo de vendedores | 7 dias | Dia de preferência: sexta; demais dias sem atendimento |
| Sem regra (segunda) | Clientes da carteira de segunda que compraram na empresa nos últimos 120 dias e no grupo nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Dia de preferência: sexta; demais dias sem atendimento |
| Prospects (terça) | Clientes da carteira de terça que nunca compraram com o próprio vendedor | 7 dias | Dia de preferência: segunda; demais dias sem atendimento |
| Alta frequência (terça) | Clientes da carteira de terça que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Dia de preferência: segunda; demais dias sem atendimento |
| Regularidade (terça) | Clientes da carteira de terça que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Dia de preferência: segunda; demais dias sem atendimento |
| Risco de inatividade (terça) | Clientes da carteira de terça que já compraram com o próprio vendedor, mas estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 7 dias | Dia de preferência: segunda; demais dias sem atendimento |
| Inativos (terça) | Clientes da carteira de terça que já compraram com o próprio vendedor, compraram na empresa nos últimos 120 dias e estão há mais de 180 dias sem comprar no grupo de vendedores | 7 dias | Dia de preferência: segunda; demais dias sem atendimento |
| Sem regra (terça) | Clientes da carteira de terça que compraram na empresa nos últimos 120 dias e no grupo nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Dia de preferência: segunda; demais dias sem atendimento |
| Prospects (quarta) | Clientes da carteira de quarta que nunca compraram com o próprio vendedor | 7 dias | Dia de preferência: terça; demais dias sem atendimento |
| Alta frequência (quarta) | Clientes da carteira de quarta que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Dia de preferência: terça; demais dias sem atendimento |
| Regularidade (quarta) | Clientes da carteira de quarta que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Dia de preferência: terça; demais dias sem atendimento |
| Risco de inatividade (quarta) | Clientes da carteira de quarta que já compraram com o próprio vendedor, mas estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 7 dias | Dia de preferência: terça; demais dias sem atendimento |
| Inativos (quarta) | Clientes da carteira de quarta que já compraram com o próprio vendedor, compraram na empresa nos últimos 120 dias e estão há mais de 180 dias sem comprar no grupo de vendedores | 7 dias | Dia de preferência: terça; demais dias sem atendimento |
| Sem regra (quarta) | Clientes da carteira de quarta que compraram na empresa nos últimos 120 dias e no grupo nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Dia de preferência: terça; demais dias sem atendimento |
| Prospects (quinta) | Clientes da carteira de quinta que nunca compraram com o próprio vendedor | 7 dias | Dia de preferência: quarta; demais dias sem atendimento |
| Alta frequência (quinta) | Clientes da carteira de quinta que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Dia de preferência: quarta; demais dias sem atendimento |
| Regularidade (quinta) | Clientes da carteira de quinta que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Dia de preferência: quarta; demais dias sem atendimento |
| Risco de inatividade (quinta) | Clientes da carteira de quinta que já compraram com o próprio vendedor, mas estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 7 dias | Dia de preferência: quarta; demais dias sem atendimento |
| Inativos (quinta) | Clientes da carteira de quinta que já compraram com o próprio vendedor, compraram na empresa nos últimos 120 dias e estão há mais de 180 dias sem comprar no grupo de vendedores | 7 dias | Dia de preferência: quarta; demais dias sem atendimento |
| Sem regra (quinta) | Clientes da carteira de quinta que compraram na empresa nos últimos 120 dias e no grupo nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Dia de preferência: quarta; demais dias sem atendimento |
| Prospects (sexta) | Clientes da carteira de sexta que nunca compraram com o próprio vendedor | 7 dias | Dia de preferência: quinta; demais dias sem atendimento |
| Alta frequência (sexta) | Clientes da carteira de sexta que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Dia de preferência: quinta; demais dias sem atendimento |
| Regularidade (sexta) | Clientes da carteira de sexta que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Dia de preferência: quinta; demais dias sem atendimento |
| Risco de inatividade (sexta) | Clientes da carteira de sexta que já compraram com o próprio vendedor, mas estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 7 dias | Dia de preferência: quinta; demais dias sem atendimento |
| Inativos (sexta) | Clientes da carteira de sexta que já compraram com o próprio vendedor, compraram na empresa nos últimos 120 dias e estão há mais de 180 dias sem comprar no grupo de vendedores | 7 dias | Dia de preferência: quinta; demais dias sem atendimento |
| Sem regra (sexta) | Clientes da carteira de sexta que compraram na empresa nos últimos 120 dias e no grupo nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Dia de preferência: quinta; demais dias sem atendimento |
| Irrestrito: prospects | Clientes da carteira irrestrita que nunca compraram com o próprio vendedor | 7 dias |  |
| Irrestrito: alta frequência | Clientes da carteira irrestrita que já compraram com o próprio vendedor e compraram no grupo de vendedores nos últimos 7 dias | 7 dias |  |
| Irrestrito: regularidade | Clientes da carteira irrestrita que já compraram com o próprio vendedor e compraram no grupo nos últimos 45 dias, mas estão há mais de 7 dias sem comprar | 14 dias |  |
| Irrestrito: risco de inatividade, curva A | Clientes da carteira irrestrita, curva A com a empresa, que já compraram com o próprio vendedor e estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 14 dias |  |
| Irrestrito: risco de inatividade, curva B | Clientes da carteira irrestrita, curva B com a empresa, que já compraram com o próprio vendedor e estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 30 dias |  |
| Irrestrito: risco de inatividade, curva C | Clientes da carteira irrestrita, curva C com a empresa, que já compraram com o próprio vendedor e estão há mais de 120 dias sem comprar com qualquer vendedor da empresa | 30 dias |  |
| Irrestrito: inativos | Clientes da carteira irrestrita que já compraram com o próprio vendedor e estão há mais de 180 dias sem comprar no grupo; os parados há mais de 120 dias na empresa, só se fora das curvas A, B e C | 21 dias | Inclui quem comprou na empresa nos últimos 120 dias |
| São José do Rio Preto | Clientes de SAO JOSE DO RIO PRETO fora de todas as carteiras, ou da carteira irrestrita que compraram no grupo nos últimos 180 dias e estão há mais de 45 dias sem comprar com o próprio vendedor | 30 dias | Na carteira irrestrita, os parados há mais de 120 dias na empresa só entram se fora das curvas A, B e C |
| Irrestrito: demais cidades | Clientes de cidade diferente de SAO JOSE DO RIO PRETO fora de todas as carteiras, ou da carteira irrestrita que compraram no grupo nos últimos 180 dias e estão há mais de 45 dias sem comprar com o próprio vendedor | 30 dias | Na carteira irrestrita, os parados há mais de 120 dias na empresa só entram se fora das curvas A, B e C |
| Prospects | Clientes que nunca compraram com qualquer vendedor da empresa | 14 dias |  |
| Ativos (1 a 7 dias) | Clientes que compraram nos últimos 7 dias | 21 dias |  |
| Ativos (8 a 30 dias) | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 30 dias |  |
| Ativos (31 a 60 dias) | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 45 dias |  |
| Ativos (61 a 90 dias) | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 70 dias |  |
| Ativos (91 a 180 dias) | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 15 dias |  |
| Inativos (acima de 180 dias) | Clientes que já compraram com qualquer vendedor da empresa e nunca compraram no grupo de vendedores ou estão há mais de 180 dias sem comprar no grupo | 21 dias | Regra final do time televendas_1: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A cascata mistura escopos de recência de compra (empresa: Risco Inatividade Segunda, Terca e Quarta; grupo: Inativos Segunda, Terca e Quarta; vendedor: Alta Frequencia Segunda, Regularidade Segunda e Alta Frequencia Terca), então as faixas podem se sobrepor ou deixar lacunas.
