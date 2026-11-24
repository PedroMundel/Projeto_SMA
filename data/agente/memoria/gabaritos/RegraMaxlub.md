```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Não agendar inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Não agendar clientes em rota":
    do time("televendas")
    quando data da rota na semana
    nao agendar

parametros "Clientes Ativos":
    do time("televendas")
    quando atividade de 60 dias
    e inatividade de 60 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando atividade de 90 dias
    e inatividade de 60 dias
    frequencia de 7 dias

parametros "Inativos (90 dias)":
    do time("televendas")
    quando atividade de 120 dias
    e inatividade de 90 dias
    frequencia de 14 dias

parametros "Inativos (120 dias)":
    do time("televendas")
    quando atividade de 150 dias
    e inatividade de 120 dias
    frequencia de 21 dias

parametros "Inativos (150 dias)":
    do time("televendas")
    quando atividade de 180 dias
    e inatividade de 150 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando prospects da empresa
    frequencia de 14 dias
```

Capacidade de atendimento: o GoBR não tem cláusula para limitar quantidade de agendamentos por dia. O número 35 ficou de fora porque não há sintaxe correspondente no manual ou exemplos.

Divergências entre o pedido e as regras (conferente):
- "Clientes Ativos": A regra seleciona clientes que compraram nos últimos 60 dias mas estão há pelo menos 60 dias sem comprar (inativos há 60 dias), enquanto o pedido pede clientes ativos com compra entre 0 e 60 dias (geralmente implica inatividade menor que 60 dias ou compra recente, não inatividade exata de 60 dias).… (pedido: "Clientes Ativos: Clientes com compra entre 0 e 60 dias, 14 dias, Somente clientes que não estão na rota da semana")

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 35.