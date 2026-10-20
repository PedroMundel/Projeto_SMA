# regra_061.gobr

Regra de frequência aplicada a três carteiras fixas: Gesiane, campo e televendas. Todas as faixas de frequência usam 14 dias. Nas carteiras de campo e de televendas, não são agendados os inativos inadimplentes, e em televendas também os clientes sem vendas. A última regra de campo e a de televendas cobrem os demais clientes, ativos ou inativos.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira Gesiane | Carteira fixa dos vendedores do time Gesiane (vendedor de id 16) |
| carteira campo | Carteira fixa de todos os vendedores de campo |
| carteira televendas | Carteira fixa de todos os vendedores de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos (Gesiane) | Clientes inativos para o vendedor | 14 dias |  |
| Sem venda (Gesiane) | Clientes que nunca compraram com o vendedor | 14 dias |  |
| Ativos (Gesiane) | Clientes ativos para o vendedor | 14 dias |  |
| Bloqueio: inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Demais clientes (campo) | Clientes ativos ou inativos para o vendedor | 14 dias | Regra final da carteira de campo: vale para quem sobrou da regra anterior |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Bloqueio: sem venda (televendas) | Clientes que nunca compraram com o vendedor | Não agendar |  |
| Demais clientes (televendas) | Clientes ativos ou inativos para o vendedor | 14 dias | Regra final da carteira de televendas: vale para quem sobrou das regras anteriores |
