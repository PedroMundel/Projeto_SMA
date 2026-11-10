```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

# BLOQUEIOS

parametros "Não agendar inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Não agendar clientes com rota do externo na semana":
    do time("televendas")
    quando data da rota do vendedor externo na semana
    nao agendar

# SEGMENTAÇÃO E PARAMETRIZAÇÕES

parametros "Clientes Ativos":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    quando fora da recencia de positivacao global em 60 dias
    frequencia de 7 dias

parametros "Inativos (90 dias)":
    do time("televendas")
    quando recencia de positivacao global em 120 dias
    quando fora da recencia de positivacao global em 90 dias
    frequencia de 14 dias

parametros "Inativos (120 dias)":
    do time("televendas")
    quando recencia de positivacao global em 150 dias
    quando fora da recencia de positivacao global em 120 dias
    frequencia de 21 dias

parametros "Inativos (150 dias)":
    do time("televendas")
    quando recencia de positivacao global em 180 dias
    quando fora da recencia de positivacao global em 150 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 14 dias

# OBSERVAÇÕES SOBRE O QUE FICOU DE FORA:
# Capacidade de atendimento: 35 clientes (Dia): o GoBR não tem cláusula para limitar a quantidade de clientes agendados por dia/vendedor.
```

Erros que ficaram depois de 2 tentativas:
- Números do pedido ausentes nas cláusulas do GoBR: 35. Ponha cada um numa cláusula ou, se o GoBR não o expressa, diga depois do código o que ficou de fora, com o número.