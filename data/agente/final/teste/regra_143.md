```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Nao agendar filiais":
    do time("televendas")
    quando e o cliente filial
    nao agendar

parametros "Nao agendar compra nos ultimos 30 dias":
    do time("televendas")
    quando recencia de positivacao global em 30 dias
    nao agendar

parametros "Prospects":
    do time("televendas")
    quando prospects da empresa
    frequencia de 28 dias

parametros "Ativos sem compra ate 44 dias":
    do time("televendas")
    quando recencia de positivacao global em 44 dias
    e fora da recencia de positivacao global em 30 dias
    frequencia de 14 dias

parametros "Ativos sem compra Curva A":
    do time("televendas")
    quando fora da recencia de positivacao global em 45 dias
    e curva A com a empresa
    frequencia de 7 dias

parametros "Ativos sem compra Curva B":
    do time("televendas")
    quando fora da recencia de positivacao global em 45 dias
    e curva B com a empresa
    frequencia de 14 dias

parametros "Ativos sem compra Curva C":
    do time("televendas")
    quando fora da recencia de positivacao global em 45 dias
    e fora da curva A com a empresa
    e fora da curva B com a empresa
    frequencia de 21 dias

parametros "Inativos":
    do time("televendas")
    quando inativos para a empresa
    frequencia de 7 dias
```

Ativos sem compra (45 dias): o GoBR não tem cláusula para "exatamente 45 dias" e a descrição do pedido era logicamente contraditória ("compraram nos últimos 45 dias" e "há pelo menos 45 dias sem comprar"). Removi este segmento.
Ativos sem compra (Curva C): o GoBR não tem a cláusula "fora da curva C". Usei a lógica de que, por ordem de execução, se o cliente não é Curva A nem Curva B, ele é Curva C (ou sem curva). A cláusula `fora da curva A com a empresa e fora da curva B com a empresa` foi mantida, mas note que não há uma cláusula explícita "fora da curva C".

Erros que ficaram depois de 3 entregas:
- R7: trecho não reconhecido: fora da curva a com a empresa. Essa cláusula não existe no GoBR desse jeito. Se não souber a forma certa, procure com buscar_manual ou buscar_exemplos pelo critério e mantenha o filtro. Só se o GoBR não tiver cláusula para isso, tire o trecho e diga nas notas o que ficou de fora, com o número.
- R7: trecho não reconhecido: fora da curva b com a empresa. Essa cláusula não existe no GoBR desse jeito. Se não souber a forma certa, procure com buscar_manual ou buscar_exemplos pelo critério e mantenha o filtro. Só se o GoBR não tiver cláusula para isso, tire o trecho e diga nas notas o que ficou de fora, com o número.

Pontos de atenção na modelagem:
- Ativos sem compra Curva C: Trecho não reconhecido (possível erro de sintaxe): fora da curva a com a empresa
- Ativos sem compra Curva C: Trecho não reconhecido (possível erro de sintaxe): fora da curva b com a empresa

Perguntas feitas:
- O segmento "Ativos sem compra (45 dias)" diz "compraram nos últimos 45 dias, mas estão há pelo menos 45 dias sem comprar". Isso é logicamente impossível. A intenção era "clientes com inatividade de exatamente 45 dias" (o GoBR não tem filtro de exatidão) ou "clientes com inatividade de 45 dias ou mais" (que seria capturado por `fora da recencia de positivacao global em 45 dias`)? Ou seria "compraram há mais de 45 dias, mas menos de X dias"? Por favor, esclareça o critério correto para este segmento. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- O segmento "Ativos sem compra (45 dias)" tem uma contradição lógica ("compraram nos últimos 45 dias" e "há pelo menos 45 dias sem comprar"). A intenção era criar um segmento para clientes com inatividade de exatamente 45 dias (o GoBR não suporta exatidão) ou era para capturar clientes que estão na fronteira entre "até 44 dias" e "mais de 45 dias"? Sugiro remover este segmento contraditório. Confirma a remoção? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.