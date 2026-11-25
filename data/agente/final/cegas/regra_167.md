```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Baixado na Receita":
    do time("televendas")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Prospect":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Única compra":
    do time("televendas")
    quando unica compra com a empresa
    frequencia de 15 dias

parametros "Ativo (comprou nos últimos 30 dias)":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 7 dias

parametros "Entre 31 e 90 dias":
    do time("televendas")
    quando recencia de positivacao entre 31 dias e 90 dias
    frequencia de 28 dias

parametros "Entre 91 e 120 dias":
    do time("televendas")
    quando recencia de positivacao entre 91 dias e 120 dias
    frequencia de 45 dias

parametros "Sem venda há 120 dias":
    do time("televendas")
    quando fora da recencia de positivacao em 120 dias
    frequencia de 60 dias
```

**Notas e Premissas:**

1.  **Frequência do Histórico (Ativo):** O GoBR não suporta cláusulas de limite dinâmico como `no minimo` ou `no maximo` diretamente na frequência de agendamento para regras padrão. A solicitação "frequência do histórico, no mínimo 7 e no máximo 21 dias" não pôde ser implementada exatamente como descrita. Foi aplicada uma frequência fixa de **7 dias** (o mínimo solicitado) para o segmento "Ativo". *O GoBR não tem cláusula para impor limites dinâmicos de frequência baseados no histórico individual dentro da regra de agendamento simples.*
2.  **Faixas de Recência (31-90, 91-120):** Utilizei a cláusula `recencia de positivacao entre X dias e Y dias`, que é a forma correta no GoBR para definir intervalos fechados de tempo desde a última compra, resolvendo o problema de "inalcançável" das regras anteriores.
3.  **Única Compra:** Utilizei a cláusula `unica compra com a empresa`, encontrada nos exemplos, para identificar o segmento.
4.  **Sem venda há 120 dias:** Utilizei `fora da recencia de positivacao em 120 dias` para capturar clientes com mais de 120 dias sem compra.

Divergências entre o pedido e as regras (conferente):
- "Ativo (comprou nos últimos 30 dias)": O pedido pede uma frequência dinâmica entre 7 e 21 dias, mas a regra aplica uma frequência fixa de 7 dias, ignorando a parte superior da faixa e a natureza dinâmica solicitada. (pedido: "Ativo (comprou nos últimos 30 dias): frequência do histórico, no mínimo 7 e no máximo 21 dias")

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Prospect": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "Única compra": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "Ativo (comprou nos últimos 30 dias)": de quantos em quantos dias agendar?
- Lacuna do pedido sem resposta do usuário: "Entre 31 e 90 dias": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "Entre 91 e 120 dias": quem são esses clientes (o critério)?
- Lacuna do pedido sem resposta do usuário: "Sem venda há 120 dias": quem são esses clientes (o critério)?
- Números do pedido que ficaram de fora do GoBR (ver notas): 21.
- A correção pedida pelo conferente não passou no validador; esta é a última versão que passou.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Prospect": quem são esses clientes (o critério)?
- "Única compra": quem são esses clientes (o critério)?
- "Ativo (comprou nos últimos 30 dias)": de quantos em quantos dias agendar?
- "Entre 31 e 90 dias": quem são esses clientes (o critério)?
- "Entre 91 e 120 dias": quem são esses clientes (o critério)?
- "Sem venda há 120 dias": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.