# regra_061.gobr

Regra padrão aplicada a três carteiras fixas: a da vendedora Gesiane, a do time de campo e a do time de televendas. A carteira da Gesiane agenda ativos, inativos e clientes sem venda a cada 14 dias. Campo e televendas também usam 14 dias para os clientes que não são bloqueados. Deixam de ser agendados os inativos inadimplentes de campo e de televendas e, em televendas, os clientes sem venda.

## Carteiras

| Carteira | Descrição |
|---|---|
| carteira Gesiane | Carteira fixa da vendedora Gesiane |
| carteira campo | Carteira fixa de todos os vendedores de campo |
| carteira televendas | Carteira fixa de todos os vendedores de televendas |

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Inativos (Gesiane) | Clientes inativos para o vendedor | 14 dias |  |
| Sem venda (Gesiane) | Clientes sem vendas para o vendedor | 14 dias |  |
| Ativos (Gesiane) | Clientes ativos para o vendedor | 14 dias |  |
| Bloqueio: inativos inadimplentes (campo) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Demais clientes (campo) | Clientes que não são inativos para o vendedor ou que são inativos para o vendedor | 14 dias | Regra final de campo: vale para quem sobrou do bloqueio anterior |
| Bloqueio: inativos inadimplentes (televendas) | Clientes inadimplentes e inativos para o vendedor | Não agendar |  |
| Bloqueio: sem venda (televendas) | Clientes sem vendas para o vendedor | Não agendar |  |
| Demais clientes (televendas) | Clientes ativos ou inativos para o vendedor | 14 dias | Regra final de televendas: vale para quem sobrou dos bloqueios anteriores |
