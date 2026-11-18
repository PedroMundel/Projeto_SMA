```gobr
version 1.0

time "padrao":
    vendedores todos

parametros "Ativos: compra nos últimos 30 dias":
    do time("padrao")
    quando atividade do vendedor de 30 dias
    frequencia de 14 dias

parametros "Inativos: sem compra há mais de 30 dias":
    do time("padrao")
    quando inativos para o vendedor
    frequencia de 14 dias
```