```gobr
version 1.0

time "time televendas":
    vendedores todostelevendas

carteira "carteira televendas":
    clientes carteirafixa("time televendas")

parametros "Não agendar clientes DH sem crédito":
    da carteira("carteira televendas")
    quando nao tem credito e tipo de cobranca igual("DH")
    nao agendar

parametros "Não agendar clientes BK com menos de R$ 199 de crédito":
    da carteira("carteira televendas")
    quando com menos de R$ 199 de credito disponivel e tipo de cobranca igual("BK")
    nao agendar

parametros "Não agendar clientes inadimplentes":
    da carteira("carteira televendas")
    quando inadimplentes
    nao agendar

parametros "Ativos 7 dias":
    da carteira("carteira televendas")
    quando ativos para o vendedor
    frequencia de 7 dias

parametros "Inativos 14 dias":
    da carteira("carteira televendas")
    quando inativos para o vendedor
    frequencia de 14 dias

parametros "Sem venda 14 dias":
    da carteira("carteira televendas")
    quando sem venda
    frequencia de 14 dias
```

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Ativos": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "inativos": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "sem venda": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
- "inativos": quem são esses clientes (o critério)?
- "sem venda": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.