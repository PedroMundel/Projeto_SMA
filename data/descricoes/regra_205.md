# regra_205.gobr

Regra de agendamento do time de televendas, com quatro carteiras fixas de rota por cidade (quinta ou segunda, terça, quarta e sexta). Primeiro são tratados os prospects e os inativos do grupo de vendedores; depois, os clientes ativos de cada rota são atendidos semanalmente no dia de preferência da rota. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| rota_quinta_segunda | Carteira fixa dos vendedores de televendas, com clientes da cidade de PONTA GROSSA |
| rota_terca | Carteira fixa dos vendedores de televendas, com clientes das cidades ARAPOTI, GUAMIRANGA, IMBITUVA, IPIRANGA, ITARARe, IVAI e mais 6 |
| rota_quarta | Carteira fixa dos vendedores de televendas, com clientes das cidades CACADOR, CANDIDO DE ABREU, CANOINHAS, IMBAU, LAPA, ORTIGUEIRA e mais 10 |
| rota_sexta | Carteira fixa dos vendedores de televendas, com clientes das cidades ADRINOPOLIS, AGUDOS DO SUL, ALMIRANTE TAMANDARE, ARAUCARIA, BALSA NOVA, BOCAIUVA DO SUL e mais 37 |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Prospects | Clientes que nunca compraram com o próprio vendedor | 28 dias |  |
| Inativos | Clientes que já compraram com o próprio vendedor, mas estão há mais de 90 dias sem comprar no grupo de vendedores | 14 dias |  |
| Ativos - rota quinta ou segunda | Clientes da carteira rota_quinta_segunda que compraram no grupo de vendedores nos últimos 90 dias e já compraram com o próprio vendedor | 7 dias | Preferência: segunda e quinta; demais dias sem atendimento |
| Ativos - rota terça | Clientes da carteira rota_terca que compraram no grupo de vendedores nos últimos 90 dias e já compraram com o próprio vendedor | 7 dias | Preferência: terça; demais dias sem atendimento |
| Ativos - rota quarta | Clientes da carteira rota_quarta que compraram no grupo de vendedores nos últimos 90 dias e já compraram com o próprio vendedor | 7 dias | Preferência: quarta; demais dias sem atendimento |
| Ativos - rota sexta | Clientes da carteira rota_sexta que compraram no grupo de vendedores nos últimos 90 dias e já compraram com o próprio vendedor | 7 dias | Preferência: sexta; demais dias sem atendimento |

## Pontos de atenção

- Clientes que compraram no grupo de vendedores nos últimos 90 dias, já compraram com o próprio vendedor e estão fora das carteiras rota_quarta, rota_quinta_segunda, rota_sexta e rota_terca não se enquadram em nenhuma regra e ficam sem parametrização.
- As carteiras rota_terca e rota_sexta compartilham 4 valores de nome de cidade (IMBITUVA, IPIRANGA, IVAI, PRUDENTOPOLIS): esses clientes aparecem nas duas.
- As carteiras rota_quarta e rota_sexta compartilham 1 valor de nome de cidade (LAPA): esses clientes aparecem nas duas.
