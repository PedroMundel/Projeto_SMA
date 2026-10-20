# regra_135.gobr

Regra de agendamento de dois times de televendas. O time de vendedores de id 0000002 atende seis carteiras fixas por cidade (segunda a sexta e irrestrito); nas de segunda a sexta, as faixas são prospects, alta frequência, regularidade, risco de inatividade, inativos e sem regra, todas com frequência de 7 dias e um dia de preferência por carteira. A carteira irrestrito tem faixas próprias de 7 a 30 dias e duas regras finais por cidade. Os demais vendedores seguem sete faixas pelo tempo desde a última compra, com regra final para os inativos. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| segunda_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2, com clientes de AGUAS DE SAO PEDRO, AMERICANA, ARARAS, CHARQUEADA, CORDEIROPOLIS, Cordeirópolis e mais 10 cidades |
| terca_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2, com clientes de AMERICO BRASILIENSE, ARARAQUARA, BARRINHA, CRAVINHOS, DESCALVADO, GUARIBA e mais 15 cidades |
| quarta_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2, com clientes de AGUAI, AGUAS DE LINDOIA, AMPARO, ANDRADAS, ARTUR NOGUEIRA, ENGENHEIRO COELHO e mais 17 cidades |
| quinta_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2, com clientes de ALUMINIO, ARACOIABA DA SERRA, BOITUVA, CERQUILHO, COTIA, IBIUNA e mais 15 cidades |
| sexta_feira_televendas_2 | Carteira fixa dos vendedores do time televendas_2, com clientes de ATIBAIA, BRAGANCA PAULISTA, CAMPINAS, CAMPO LIMPO PAULISTA, COSMOPOLIS, HORTOLANDIA e mais 9 cidades |
| irrestrito_televendas_2 | Carteira fixa dos vendedores do time televendas_2, com clientes de ARUJA, BARUERI, CAIEIRAS, CAJAMAR, CARAPICUIBA, DIADEMA e mais 19 cidades |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects (segunda) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Alta frequência (segunda) | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Regularidade (segunda) | Clientes que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Risco de inatividade (segunda) | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Inativos (segunda) | Clientes que compraram na empresa nos últimos 120 dias, estão há mais de 180 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Sem regra (segunda) | Clientes que compraram na empresa nos últimos 120 dias e no grupo de vendedores nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Preferência de atendimento na sexta; demais dias sem atendimento |
| Prospects (terça) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Alta frequência (terça) | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Regularidade (terça) | Clientes que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Risco de inatividade (terça) | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Inativos (terça) | Clientes que compraram na empresa nos últimos 120 dias, estão há mais de 180 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Sem regra (terça) | Clientes que compraram na empresa nos últimos 120 dias e no grupo de vendedores nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Preferência de atendimento na segunda; demais dias sem atendimento |
| Prospects (quarta) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Alta frequência (quarta) | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Regularidade (quarta) | Clientes que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Risco de inatividade (quarta) | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Inativos (quarta) | Clientes que compraram na empresa nos últimos 120 dias, estão há mais de 180 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Sem regra (quarta) | Clientes que compraram na empresa nos últimos 120 dias e no grupo de vendedores nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Preferência de atendimento na terça; demais dias sem atendimento |
| Prospects (quinta) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Alta frequência (quinta) | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Regularidade (quinta) | Clientes que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Risco de inatividade (quinta) | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Inativos (quinta) | Clientes que compraram na empresa nos últimos 120 dias, estão há mais de 180 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Sem regra (quinta) | Clientes que compraram na empresa nos últimos 120 dias e no grupo de vendedores nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Preferência de atendimento na quarta; demais dias sem atendimento |
| Prospects (sexta) | Clientes que nunca compraram com o próprio vendedor | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Alta frequência (sexta) | Clientes que compraram com o próprio vendedor nos últimos 30 dias | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Regularidade (sexta) | Clientes que compraram com o próprio vendedor nos últimos 45 dias, mas estão há mais de 30 dias sem comprar | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Risco de inatividade (sexta) | Clientes que estão há mais de 120 dias sem comprar com qualquer vendedor da empresa e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Inativos (sexta) | Clientes que compraram na empresa nos últimos 120 dias, estão há mais de 180 dias sem comprar no grupo de vendedores e já compraram com o próprio vendedor | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Sem regra (sexta) | Clientes que compraram na empresa nos últimos 120 dias e no grupo de vendedores nos últimos 180 dias, mas estão há mais de 45 dias sem comprar com o próprio vendedor | 7 dias | Preferência de atendimento na quinta; demais dias sem atendimento |
| Irrestrito: prospects | Clientes que nunca compraram com o próprio vendedor | 7 dias |  |
| Irrestrito: alta frequência | Clientes que compraram no grupo de vendedores nos últimos 7 dias e já compraram com o próprio vendedor | 7 dias |  |
| Irrestrito: regularidade | Clientes que compraram no grupo de vendedores nos últimos 45 dias, mas estão há mais de 7 dias sem comprar, e já compraram com o próprio vendedor | 14 dias |  |
| Irrestrito: risco de inatividade curva A | Clientes curva A com a empresa, há mais de 120 dias sem comprar com qualquer vendedor da empresa, que já compraram com o próprio vendedor | 14 dias |  |
| Irrestrito: risco de inatividade curva B | Clientes curva B com a empresa, há mais de 120 dias sem comprar com qualquer vendedor da empresa, que já compraram com o próprio vendedor | 30 dias |  |
| Irrestrito: risco de inatividade curva C | Clientes curva C com a empresa, há mais de 120 dias sem comprar com qualquer vendedor da empresa, que já compraram com o próprio vendedor | 30 dias |  |
| Irrestrito: inativos | Clientes que já compraram com o próprio vendedor e estão há mais de 180 dias sem comprar no grupo de vendedores | 21 dias | Entra quem comprou na empresa em até 120 dias ou, acima disso, quem está fora das curvas A, B e C |
| São José do Rio Preto | Clientes da cidade SAO JOSE DO RIO PRETO fora de todas as carteiras ou, na carteira irrestrito, sem regra mapeada nas faixas anteriores | 30 dias | Vale para quem sobrou das regras anteriores |
| Irrestrito: sem regra mapeada | Clientes de cidade diferente de SAO JOSE DO RIO PRETO fora de todas as carteiras ou, na carteira irrestrito, sem regra mapeada nas faixas anteriores | 30 dias | Regra final do time televendas_2: vale para quem sobrou das regras anteriores |
| Prospects | Clientes que nunca compraram na empresa | 14 dias |  |
| Ativos (1 a 7 dias) | Clientes que compraram nos últimos 7 dias | 21 dias |  |
| Ativos (8 a 30 dias) | Clientes que compraram nos últimos 30 dias, mas estão há mais de 7 dias sem comprar | 30 dias |  |
| Ativos (31 a 60 dias) | Clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar | 45 dias |  |
| Ativos (61 a 90 dias) | Clientes que compraram nos últimos 90 dias, mas estão há mais de 60 dias sem comprar | 70 dias |  |
| Ativos (91 a 180 dias) | Clientes que compraram nos últimos 180 dias, mas estão há mais de 90 dias sem comprar | 15 dias |  |
| Inativos (acima de 180 dias) | Clientes que já compraram na empresa e nunca compraram no grupo de vendedores ou estão há mais de 180 dias sem comprar nele | 21 dias | Regra final do time televendas_1: vale para quem sobrou das faixas anteriores |

## Pontos de atenção

- A sequência de regras mistura escopos de recência de compra (global em Risco Inatividade Segunda, Terca e Quarta; grupo de vendedores em Inativos Segunda, Terca e Quarta; vendedor em Alta Frequencia Segunda, Regularidade Segunda e Alta Frequencia Terca), então faixas de escopos diferentes podem se sobrepor ou deixar lacunas.
