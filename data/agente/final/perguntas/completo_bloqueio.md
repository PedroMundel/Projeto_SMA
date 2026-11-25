```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Ativos":
    do time("televendas")
    quando atividade de 60 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 60 dias
    frequencia de 21 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.