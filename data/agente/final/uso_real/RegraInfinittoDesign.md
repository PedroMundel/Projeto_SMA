```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Prospect":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Ativo":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 7 dias

parametros "Inativo":
    do time("televendas")
    frequencia de 28 dias
```

O erro "inalcançável" ocorre porque, na lógica de processamento sequencial do GoBR, as regras de "Ativo", "Risco de inatividade" e "Inativo" baseadas em `recencia` ou ausência dela cobrem todos os clientes que têm histórico de compras ou inatividade. O segmento "Prospect" (clientes que nunca compraram ou estão em ciclo de vida prospect) deve ser avaliado **antes** das regras de recência, pois a recência só se aplica a quem já comprou. Se a regra de Prospect ficar por último, nenhum cliente entrará nela, pois todos os que nunca compraram já foram capturados pela regra final de "Inativo" (que no exemplo anterior era um "catch-all" para quem sobrou, mas tecnicamente prospectos não têm recência de compra).

A correção é mover a regra "Prospect" para o início, antes das regras de Ativo, Risco e Inativo.

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.