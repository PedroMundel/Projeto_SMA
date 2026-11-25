```gobr
version 1.0

time "time vendas":
    vendedores todos

carteira "carteira vendas":
    clientes carteirafixa("time vendas")

parametros "Bloqueio: inativos inadimplentes":
    da carteira("carteira vendas")
    quando inativos para o vendedor e inadimplentes
    nao agendar

parametros "Sem vendas":
    da carteira("carteira vendas")
    quando prospects do vendedor
    frequencia de 30 dias

parametros "Ativos adimplentes":
    da carteira("carteira vendas")
    quando ativos para o vendedor e adimplentes
    frequencia de 30 dias

parametros "Ativos inadimplentes":
    da carteira("carteira vendas")
    quando ativos para o vendedor e inadimplentes
    frequencia de 60 dias

parametros "Inativos adimplentes":
    da carteira("carteira vendas")
    quando inativos para o vendedor e adimplentes
    frequencia de 60 dias
```