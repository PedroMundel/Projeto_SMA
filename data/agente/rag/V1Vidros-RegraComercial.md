```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

## Regras de não agendamento

parametros "Não agendar clientes baixados na receita":
    do time("televendas")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Não agendar inadiplentes":
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
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando atividade de 45 dias
    quando inatividade de 30 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade global de 45 dias
    frequencia de 14 dias
```

Clientes inadiplentes autorizados para agendamento: o GoBR não tem cláusula para "autorizar" inadiplentes específicos; a cláusula `nao agendar` para inadimplentes é padrão, mas não há distinção para "autorizados". Se houver uma lista específica de inadiplentes permitidos, isso não é modelável diretamente com as cláusulas atuais sem criar exceções manuais ou regras complexas não previstas.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativos; grupo: Clientes Ativos, Risco de Inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.