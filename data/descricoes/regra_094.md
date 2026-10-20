# regra_094.gobr

Regra padrão de frequência para os times de televendas e de campo, cada um com a sua carteira fixa. Em televendas, os clientes adimplentes têm frequência de 30 dias e os inadimplentes de 60 dias; a faixa de clientes sem venda de televendas nunca chega a ser aplicada. No campo, todos os clientes seguem a frequência de 30 dias. Não há regras de bloqueio.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira televendas | Carteira fixa dos vendedores do time televendas |
| carteira campo | Carteira fixa dos vendedores do time campo |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Televendas: adimplentes | Clientes adimplentes | 30 dias |  |
| Televendas: inadimplentes | Clientes inadimplentes | 60 dias |  |
| Televendas: sem venda | Clientes que nunca compraram com o vendedor | 30 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Campo: todos os clientes | Clientes de todos os perfis da carteira campo | 30 dias |  |

## Pontos de atenção

- A regra '30 dias para clientes sem venda (televendas)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
