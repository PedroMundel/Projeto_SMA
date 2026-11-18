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
    e inatividade de 0 dias
    e inatividade global de 60 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("televendas")
    quando atividade de 90 dias
    e inatividade de 60 dias
    e inatividade global de 60 dias
    frequencia de 7 dias

parametros "Inativos (90 dias)":
    do time("televendas")
    quando atividade de 120 dias
    e inatividade de 90 dias
    e inatividade global de 90 dias
    frequencia de 14 dias

parametros "Inativos (120 dias)":
    do time("televendas")
    quando atividade de 150 dias
    e inatividade de 120 dias
    e inatividade global de 120 dias
    frequencia de 21 dias

parametros "Inativos (150 dias)":
    do time("televendas")
    quando atividade de 180 dias
    e inatividade de 150 dias
    e inatividade global de 150 dias
    frequencia de 28 dias

parametros "Prospects":
    do time("televendas")
    quando prospects da empresa
    frequencia de 14 dias

parametros "Clientes não mapeados":
    do time("televendas")
    nao agendar
```

Capacidade de atendimento: 35 clientes (Dia): o GoBR não tem cláusula para limitar quantidade de clientes por dia.

Divergências entre o pedido e as regras (conferente):
- "Clientes não mapeados": A regra 'Clientes não mapeados' não corresponde a nenhum segmento ou instrução explícita no pedido de negócio. (pedido: "Nenhum trecho específico do pedido corresponde a esta regra (o pedido não menciona clientes não mapeados como segmento a ser tratado ou bloqueado explicitamente além dos já cobertos).")

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Clientes Ativos, Risco de Inatividade, Inativos (90 dias); grupo: Clientes Ativos, Risco de Inatividade, Inativos (90 dias)); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- Clientes não mapeados: Condição efetiva fragmentada demais para resumir; descreva como a condição própria exceto os clientes já tratados pelas regras anteriores.
- Números do pedido que ficaram de fora do GoBR (ver notas): 35.