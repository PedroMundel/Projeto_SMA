# regra_101.gobr

Regra de frequência para três times: televendas, capital (região metropolitana) e interior. Em cada time, a frequência depende de o cliente ser ativo, inativo ou sem venda; na capital e no interior, os inativos também se separam entre adimplentes e inadimplentes. Os clientes inativos inadimplentes da capital e do interior não são agendados.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Ativos (televendas) | Clientes do televendas ativos para o vendedor | 7 dias |  |
| Inativos (televendas) | Clientes do televendas inativos para o vendedor | 30 dias |  |
| Sem venda (televendas) | Clientes do televendas sem vendas para o vendedor | 7 dias |  |
| Ativos (região metropolitana) | Clientes da capital ativos para o vendedor | 7 dias |  |
| Inativos adimplentes (região metropolitana) | Clientes da capital adimplentes e inativos para o vendedor | 14 dias |  |
| Bloqueio: inativos inadimplentes (região metropolitana) | Clientes da capital inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem venda (região metropolitana) | Clientes da capital sem vendas para o vendedor | 14 dias |  |
| Ativos (interior) | Clientes do interior ativos para o vendedor | 14 dias |  |
| Inativos adimplentes (interior) | Clientes do interior adimplentes e inativos para o vendedor | 30 dias |  |
| Bloqueio: inativos inadimplentes (interior) | Clientes do interior inadimplentes e inativos para o vendedor | Não agendar |  |
| Sem venda (interior) | Clientes do interior sem vendas para o vendedor | 30 dias |  |
