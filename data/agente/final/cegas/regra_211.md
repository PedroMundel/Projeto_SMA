```gobr
version 1.0

time "ativacao":
    vendedores porid("970","967","973","974")

parametros "Clientes com pedido nos últimos 30 dias":
    do time("ativacao")
    quando tem venda em 30 dias
    frequencia de 21 dias

parametros "Clientes que não pediram nesse período":
    do time("ativacao")
    quando nao tem venda em 30 dias
    frequencia de 15 dias
```