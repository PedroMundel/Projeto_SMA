# regra_147.gobr

Regra de frequência por time. Os times Carteira, PetVet e Portal têm faixas para clientes novos, ativos, inativos e sem venda, com frequências de 1 a 20 dias. O time Distribuidor é organizado por curva A, B, C e clientes sem classificação, com frequências de 2 a 15 dias. O time Pré-venda atende todos os clientes a cada 7 dias. Não há regras de bloqueio.

## Regras

| Segmento | Critério | Frequência | Observação |
|---|---|---|---|
| Novos sem atendimento | Clientes cadastrados a partir de '2023-07-18' que estão há mais de 60 dias sem receber visita | 1 dia | Vale para os times Carteira, PetVet e Portal |
| Clientes novos | Clientes cadastrados a partir de '2023-07-18' que nunca foram visitados ou foram visitados nos últimos 60 dias | 7 dias | Vale para os times Carteira, PetVet e Portal |
| Clientes ativos | Clientes ativos para o vendedor, cadastrados antes de '2023-07-18' | 5 dias | Vale para os times Carteira, PetVet e Portal |
| Clientes inativos | Clientes inativos para o vendedor, cadastrados antes de '2023-07-18' | 10 dias | Vale para os times Carteira, PetVet e Portal |
| Clientes sem venda | Clientes sem vendas para o vendedor, cadastrados antes de '2023-07-18' | 20 dias | Vale para os times Carteira, PetVet e Portal |
| Curva A | Clientes curva A com o vendedor | 2 dias | Vale para o time Distribuidor |
| Curva B | Clientes curva B com o vendedor | 4 dias | Vale para o time Distribuidor |
| Curva C | Clientes curva C com o vendedor | 7 dias | Vale para o time Distribuidor |
| Sem classificação de curva | Clientes fora das curvas A, B e C com o vendedor | 15 dias | Vale para o time Distribuidor |
| Todos os clientes | Clientes sem filtro: todos os clientes do time | 7 dias | Vale para o time Pré-venda |
