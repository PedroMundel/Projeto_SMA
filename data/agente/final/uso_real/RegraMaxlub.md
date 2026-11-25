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
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando fora da recencia de positivacao global em 60 dias
    e recencia de positivacao global em 90 dias
    frequencia de 7 dias

parametros "Inativos (90 dias)":
    do time("televendas")
    quando fora da recencia de positivacao global em 90 dias
    e recencia de positivacao global em 120 dias
    frequencia de 14 dias

parametros "Inativos (120 dias)":
    do time("televendas")
    quando fora da recencia de positivacao global em 120 dias
    e recencia de positivacao global em 150 dias
    frequencia de 21 dias

parametros "Inativos (150 dias)":
    do time("televendas")
    quando fora da recencia de positivacao global em 150 dias
    e recencia de positivacao global em 180 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 14 dias

parametros "Clientes que não se enquadram":
    do time("televendas")
    nao agendar
```

Capacidade de atendimento: o GoBR não tem cláusula para limitar quantidade de clientes por dia (número 35 do pedido).
Segmento "Clientes Ativos": o critério "compra entre 0 e 60 dias" foi interpretado como "comprou nos últimos 60 dias" (padrão do manual/exemplos). A restrição de "0 dias" (excluir compra de hoje) não é suportada diretamente.
Segmento "Risco de Inatividade": o critério "compraram nos últimos 90 mas estão a 60 dias sem comprar" foi mapeado para `fora da recencia de positivacao global em 60 dias` e `recencia de positivacao global em 90 dias`. Isso captura clientes cuja última compra foi entre 61 e 90 dias atrás.
Segmento "Inativos (90/120/150 dias)": a lógica segue o padrão: `fora da recencia... em N dias` e `recencia... em M dias` para capturar o intervalo de última compra.
Segmento "Prospects": usei `prospects da empresa` conforme manual.
Bloqueios: `inadimplentes` e `data da rota na semana` aplicados antes das faixas.
Regra final: adicionada para garantir que clientes que não caem em nenhuma faixa não sejam agendados.

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 35.