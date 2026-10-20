# regra_048.gobr

Regras de frequência para duas carteiras fixas, a do time campo e a do time televendas. Em cada carteira, as faixas separam clientes ativos e inativos, adimplentes e inadimplentes, além dos clientes sem vendas, e cada grupo tem sua frequência. A regra final de prospects de cada carteira não chega a ser aplicada, pois as faixas anteriores já tratam todos os clientes. Não há bloqueios de agenda.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira campo | Carteira fixa dos vendedores do time campo |
| carteira televendas | Carteira fixa dos vendedores do time televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos adimplentes (televendas) | Clientes adimplentes e ativos para o vendedor | 14 dias |  |
| Ativos inadimplentes (televendas) | Clientes inadimplentes e ativos para o vendedor | 7 dias |  |
| Inativos adimplentes (televendas) | Clientes adimplentes e inativos para o vendedor | 30 dias |  |
| Inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | 60 dias |  |
| Sem vendas (televendas) | Clientes que nunca compraram com o vendedor | 30 dias |  |
| Prospects (televendas) | Clientes da carteira televendas, sem nenhum filtro, exceto os já tratados pelas regras anteriores | 30 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |
| Ativos adimplentes (campo) | Clientes adimplentes e ativos para o vendedor | 7 dias |  |
| Ativos inadimplentes (campo) | Clientes inadimplentes e ativos para o vendedor | 14 dias |  |
| Inativos adimplentes (campo) | Clientes adimplentes e inativos para o vendedor | 14 dias |  |
| Inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor | 30 dias |  |
| Sem vendas (campo) | Clientes que nunca compraram com o vendedor | 14 dias |  |
| Prospects (campo) | Clientes da carteira campo, sem nenhum filtro, exceto os já tratados pelas regras anteriores | 14 dias | Nunca é aplicada: todos esses clientes já foram tratados antes |

## Pontos de atenção

- A regra 'prospects (televendas)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
- A regra 'prospects (campo)' nunca é aplicada: todos os clientes dela já são tratados por regras anteriores.
