```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

## Regras de não agendamento

parametros "Não agendar clientes baixados na receita":
    do time("televendas")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Agendar Inadiplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

## Regras de agendamento

parametros "Clientes Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Clientes Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando recencia de positivacao em 45 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 14 dias
```

Clientes com critério de "30 dias sem comprar" na regra de Risco de Inatividade: o GoBR não tem cláusula para filtrar dias específicos de inatividade dentro da regra de recência máxima (usa-se apenas o teto de recência). A regra aplica-se a quem comprou nos últimos 45 dias, o que implicitamente exclui quem está há mais de 45 dias, mas não filtra especificamente o intervalo de 30-45 dias de inatividade como critério separado.