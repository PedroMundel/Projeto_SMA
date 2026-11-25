```gobr
version 1.0

time "televendas":
    vendedores todostelevendas

parametros "Não agendar clientes ativos recentes":
    do time("televendas")
    quando tem venda da empresa em 45 dias
    nao agendar

parametros "Prospect - 28 dias":
    do time("televendas")
    quando prospects da empresa
    frequencia de 28 dias

parametros "Caminhando para inatividade - 14 dias":
    do time("televendas")
    quando tem venda da empresa em 89 dias
        e não tem venda da empresa em 45 dias
    frequencia de 14 dias

parametros "Inativo para resgate - 21 dias":
    do time("televendas")
    frequencia de 21 dias
```

**Observações:**
- O pedido não especifica um critério explícito de "Prospect" (ex: nunca comprou), mas o exemplo 230 e 228 usam `no ciclo de vida prospect` ou `prospects da empresa`. Assumi `prospects da empresa` para o segmento Prospect, pois é o padrão do manual para clientes sem histórico.
- A faixa "Inativo para resgate" é a regra final (sem `quando`) para capturar os clientes que não se encaixaram nas faixas anteriores (ou seja, sem compra há mais de 89 dias).
- A ordem das regras é crucial: primeiro o bloqueio (45 dias), depois a faixa intermediária (46-89 dias) e por fim a captura geral (resto). O segmento "Prospect" foi inserido antes das faixas de recência para garantir que clientes que nunca compraram (e portanto não têm "dias sem compra" no sentido tradicional de inatividade, ou teriam uma recência muito alta) sejam tratados corretamente como prospect e não caiam na faixa de "caminhando para inatividade" ou "inativo" se a lógica de recência não os excluísse explicitamente. No entanto, `prospects da empresa` exclui quem tem compra, então a ordem entre Prospect e as faixas de recência não gera conflito de sobreposição, mas a ordem de bloqueio > faixa específica > regra ge…

Pontos de atenção na modelagem:
- Números do pedido que ficaram de fora do GoBR (ver notas): 46.