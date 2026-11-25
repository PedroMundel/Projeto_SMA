```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda do vendedor em 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inativos para o vendedor
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Os inativos a cada 28 dias.