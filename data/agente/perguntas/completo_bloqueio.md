```gobr
version 1.0

time "todos vendedores":
    vendedores todos ativados

parametros "Bloqueio: Inadimplentes":
    do time("todos vendedores")
    quando inadimplentes
    nao agendar

parametros "Ativos: clientes com pedidos nos últimos 60 dias":
    do time("todos vendedores")
    quando atividade de 60 dias
    frequencia de 7 dias

parametros "Inativos: clientes sem pedidos há mais de 60 dias":
    do time("todos vendedores")
    quando inatividade de 60 dias
    frequencia de 21 dias
```