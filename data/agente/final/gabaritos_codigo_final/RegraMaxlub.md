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
    quando atividade global de 60 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando atividade global de 90 dias
    e inatividade global de 60 dias
    frequencia de 7 dias

parametros "Inativos (90 dias)":
    do time("televendas")
    quando atividade global de 120 dias
    e inatividade global de 90 dias
    frequencia de 14 dias

parametros "Inativos (120 dias)":
    do time("televendas")
    quando atividade global de 150 dias
    e inatividade global de 120 dias
    frequencia de 21 dias

parametros "Inativos (150 dias)":
    do time("televendas")
    quando atividade global de 180 dias
    e inatividade global de 150 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando prospects da empresa
    frequencia de 14 dias
```

Capacidade de atendimento: o GoBR não tem cláusula para limitar a quantidade de agendamentos por dia (35 clientes).

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 35.