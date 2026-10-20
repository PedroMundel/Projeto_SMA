# regra_175.gobr

Regra do time de televendas aplicada a uma carteira fixa de clientes de determinados ramos de atividade. Deixam de ser agendados os clientes filiais, os inadimplentes e os que compraram nos últimos 30 dias. Os demais seguem frequência de 14 dias (ativos da empresa) ou 21 dias (inativos), com faixas de 21 e 30 dias para quem teve compra em períodos anteriores e está sem vendas. A regra final não agenda quem sobrou, inclusive quem está fora da carteira.

## Carteiras

| Carteira | Descrição |
|---|---|
| activity_in | Carteira fixa dos vendedores do time televendas, filtrada pelos ramos de atividade 1, 18, 2, 23, 3, 4 e mais 1 ramo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Bloqueio: filiais | Clientes que são filiais | Não agendar |  |
| Bloqueio: inadimplentes | Clientes inadimplentes | Não agendar |  |
| Bloqueio: compra nos últimos 30 dias | Clientes que compraram nos últimos 30 dias | Não agendar |  |
| Ativos na empresa | Clientes ativos para a empresa | 14 dias |  |
| Inativos na empresa | Clientes inativos para a empresa | 21 dias |  |
| Compraram no ano anterior, sem compra no ano atual | Clientes que compraram com a empresa no ano anterior, não compraram no ano atual e não têm vendas para a empresa | 21 dias |  |
| Compraram em período anterior e pararam | Clientes sem vendas para a empresa, com compra no intervalo entre <d0> e <d1>, exceto os já tratados pelas regras anteriores | 30 dias |  |
| Bloqueio: demais clientes | Clientes fora da carteira activity_in e, dentro dela, clientes sem vendas para a empresa que não se encaixam nas faixas de compra anteriores | Não agendar | Regra final: vale para quem sobrou das regras anteriores |
