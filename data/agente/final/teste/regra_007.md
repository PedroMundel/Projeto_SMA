```gobr
version 1.0

time "time todos":
    vendedores todos

carteira "carteira todos":
    clientes carteirafixa("time todos")

parametros "Inativos":
    da carteira("carteira todos")
    quando inativos para o vendedor
    frequencia de 30 dias

parametros "Ativos":
    da carteira("carteira todos")
    quando ativos para o vendedor
    frequencia de 14 dias

parametros "Sem vendas":
    da carteira("carteira todos")
    quando sem venda
    frequencia de 7 dias
```