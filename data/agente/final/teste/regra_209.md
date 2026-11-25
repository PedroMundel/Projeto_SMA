```gobr
version 1.0


time "televendas":
    vendedores todos ativados


parametros "Bloqueio: inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Bloqueio: filiais":
    do time("televendas")
    quando cliente filial
    nao agendar

parametros "Bloqueio: fora de recencia 90 dias":
    do time("televendas")
    quando fora da recencia de positivação do vendedor há 90 dias atras
    nao agendar


parametros "Novos clientes":
    do time("televendas")
    quando prospects do vendedor
    frequencia de 7 dias

parametros "Compra com regularidade":
    do time("televendas")
    quando atividade do vendedor de 30 dias
        e frequencia historica menor que 30 dias
    frequencia de 7 dias

parametros "Precisa de acompanhamento":
    do time("televendas")
    quando atividade do vendedor de 30 dias
        e frequencia historica maior que 30 dias
    frequencia de 17 dias
```

**Observações:**

1.  **Bloqueio fora de recência:** A cláusula `fora da recencia de positivação do vendedor há 90 dias atras` foi usada para capturar clientes há mais de 90 dias sem comprar com o próprio vendedor, conforme a sintaxe de condicionais de tempo do manual.
2.  **Frequência Histórica Indefinida:** O pedido original solicitava agrupar "frequência histórica indefinida ou de mais de 30 dias" na regra "Precisa de acompanhamento". O manual do GoBR oferece `frequencia historica maior que <<N>> dias` e `frequencia historica menor que <<N>> dias ou indefinida`, mas não oferece um filtro direto para "maior que N ou indefinida". Para manter a fidelidade aos filtros disponíveis e evitar sobreposição com a regra de "Regularidade" (que usa `menor que 30 dias`), a regra de "Acompanhamento" foi escrita com `frequencia historica maior que 30 dias`.
    *   *Nota:* Clientes com frequência histórica **indefinida** que compraram nos últimos 30 dias podem não ser capturados por nenhuma das duas regras de agendamento (nem pela de regularidade, que pede `menor que 30`, nem pela de acompanhamento, que pede `maior que 30`), a menos que o motor do GoBR trate `menor que 30` como excluindo indefi…
- "Clientes que compraram com o próprio vendedor nos últimos 30 dias e têm frequência histórica indefinida": O GoBR não tem uma cláusula `frequencia historica indefinida` isolada nem `frequencia historica maior que 30 dias ou indefinida`. A cláusula `frequencia historica menor que 30 dias ou indefinida` existe, mas não permite separar os indefinidos dos de baixa frequência sem sobreposição. Portanto, clientes com frequência indefinida não são capturados pelas regras de agendamento fornecidas.

Divergências entre o pedido e as regras (conferente):
- "Precisa de acompanhamento": A regra exclui clientes com frequência histórica indefinida, enquanto o pedido solicita que eles sejam incluídos na regra de acompanhamento. (pedido: "Precisa de acompanhamento: Clientes que compraram com o próprio vendedor nos últimos 30 dias e têm frequência histórica indefinida ou de mais de 30 dias, 17 dias")

Pontos de atenção na modelagem:
- A correção pedida pelo conferente não passou no validador; esta é a última versão que passou.