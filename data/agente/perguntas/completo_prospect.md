```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Prospects":
    do time("televendas")
    quando prospects da empresa
    frequencia de 7 dias

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 90 dias
    frequencia de 14 dias

parametros "Demais clientes":
    do time("televendas")
    frequencia de 30 dias
```

**Premissas e Observações:**
1. Assumi o time "televendas" e o filtro `prospects da empresa` com base nos exemplos fornecidos (regra_149 e regra_077), pois o pedido não especificou o time nem a sintaxe exata do filtro de ciclo de vida.
2. O critério "Demais clientes" foi implementado como uma regra final sem cláusula `quando`, capturando todos os clientes que não se encaixaram nas regras anteriores (não são prospects e não compraram nos últimos 90 dias).
3. O pedido não especificou bloqueios (como "não agendar se comprou ontem"), portanto, nenhuma cláusula `nao agendar` foi incluída.