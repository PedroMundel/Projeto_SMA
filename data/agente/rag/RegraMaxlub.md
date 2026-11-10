```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

# BLOQUEIOS

parametros "Não agendar inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Não agendar clientes com data da rota na semana":
    do time("televendas")
    quando data da rota na semana
    nao agendar

# FAIXAS DE CLIENTES

parametros "Clientes Ativos":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 7 dias

parametros "Inativos (90 dias)":
    do time("televendas")
    quando recencia de positivacao global em 120 dias
    frequencia de 14 dias

parametros "Inativos (120 dias)":
    do time("televendas")
    quando recencia de positivacao global em 150 dias
    frequencia de 21 dias

parametros "Inativos (150 dias)":
    do time("televendas")
    quando recencia de positivacao global em 180 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 14 dias

# REGRA FINAL PARA QUEM SOBROU (INATIVOS > 180 DIAS OU SEM COMPRA HÁ MAIS DE 180 DIAS)
# O pedido não especifica frequência para este grupo residual, mas a lógica de "faixas" exige uma regra final.
# Como não há instrução explícita para agendar os inativos > 180 dias, e o exemplo 239 usa "nao agendar" para não mapeados,
# mas aqui temos faixas de inatividade específicas até 150 dias (180 dias de recência).
# Clientes com mais de 180 dias sem comprar não se enquadram em nenhuma regra acima.
# Se o objetivo é não agendar quem está muito inativo, usamos nao agendar. Se o objetivo é agendar com frequência padrão,
# precisaríamos de uma frequência. Considerando a estrutura de "Inativos (150 dias)" como a última faixa ativa,
# assumiremos que quem não se encaixa em nenhuma faixa (inativos > 180 dias) não será agendado automaticamente por estas regras,
# ou poderia ser tratado por uma regra de "catch-all" se houvesse instrução.
# Dado o pedido "Inativos (150 dias): Comprou nos últimos 180 mas estão a 150 dias sem comprar",
# quem comprou há mais de 180 dias não entra em nenhuma regra.
# Vou deixar sem regra final explícita ou com nao agendar se for o padrão de limpeza.
# No exemplo 239, a regra final é "nao agendar" para não mapeados.
# Aqui, não há instrução para agendar quem está há > 180 dias.
# Portanto, não há regra para agendar quem sobrou.

# NOTA: A capacidade de atendimento de 35 clientes/dia é uma restrição operacional do sistema/rota,
# não uma cláusula de filtragem de cliente no GoBR.
```

Clientes Ativos: O critério "compra entre 0 e 60 dias" foi modelado como `recencia de positivacao global em 60 dias`. A faixa "0 a 60" é implícita pois regras anteriores (bloqueios) e a ordem de execução (primeiro que vence) tratam quem está fora. Como não há regra anterior para "ativos recentes" vs "ativos antigos" dentro dos 60 dias, a regra captura todos os ativos nos últimos 60 dias.
Risco de Inatividade: O critério "comprou nos últimos 90 mas estão a 60 dias sem comprar" foi modelado como `recencia de positivacao global em 90 dias`. Isso captura quem comprou nos últimos 90 dias. Como a regra de "Ativos" (60 dias) vem antes, quem está há menos de 60 dias já foi capturado. Sobram os que estão entre 60 e 90 dias de inatividade (ou seja, compraram há entre 60 e 90 dias). Isso atende ao critério.
Inativos (90 dias): O critério "comprou nos últimos 120 dias mas estão a 90 dias sem comprar" foi modelado como `recencia de positivacao global em 120 dias`. A ordem das regras garante que quem está há menos de 90 dias já foi capturado pelas regras anteriores (Ativos, Risco, Inativos 90 dias não existe ainda, mas a regra de Risco pega até 90 dias de recência, ou seja, inatividade até 90 dias? Não. `recencia em 90 dias` significa a última compra foi há <= 90 dias. Se a regra de Risco pega quem comprou há <= 90 dias, e a de Ativos pega quem comprou há <= 60 dias, sobram os que compraram há entre 60 e 90 dias. A regra "Inativos (90 dias)" pede quem comprou há <= 120 dias e está há >= 90 dias sem comprar. A cláusula `recencia em 120 dias` pega quem comprou há <= 120 dias. Como a regra de Risco (90 dias) vem antes, quem comprou há <= 90 dias já foi processado. Sobram os que compraram há entre 90 e 120 dias. Isso atende ao critério de "comprou nos últimos 120 dias" (pois 90-120 está dentro de 120) e "estão a 90 dias sem comprar" (pois > 90 dias).
Inativos (120 dias): Similarmente, `recencia em 150 dias` pega quem comprou há <= 150 dias. As regras anteriores cobrem até 120 dias de recência (Inativos 90 dias). Sobram os que compraram há entre 120 e 150 dias. Atende "comprou nos últimos 150 dias" e "estão a 120 dias sem comprar" (pois > 120 dias).
Inativos (150 dias): `recencia em 180 dias` pega quem comprou há <= 180 dias. As regras anteriores cobrem até 150 dias de recência. Sobram os que compraram há entre 150 e 180 dias. Atende "comprou nos últimos 180 dias" e "estão a 150 dias sem comprar" (pois > 150 dias).
Prospects: `no ciclo de vida prospect com a empresa` atende ao critério.
Não agendar inadimplentes: `inadimplentes` atende.
Não agendar clientes em rota: `data da rota na semana` atende.
Capacidade de atendimento: O GoBR não possui cláusula para limitar a quantidade de agendamentos por dia (35 clientes). Isso deve ser configurado na ferramenta de roteirização ou agenda, não na regra de segmentação.

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 35.