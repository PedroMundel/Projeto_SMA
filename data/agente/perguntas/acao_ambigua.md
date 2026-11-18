```gobr
version 1.0

time "time padrao":
    vendedores todos

parametros "Inadimplentes":
    do time("time padrao")
    quando inadimplentes
    nao agendar

parametros "Ativos":
    do time("time padrao")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("time padrao")
    frequencia de 28 dias
```

**Observações:**
1. "Tratar à parte" foi interpretado como `nao agendar` (bloqueio), seguindo o padrão do exemplo `regra_194` para clientes que não devem ser contatados automaticamente.
2. O critério "compra nos últimos 60 dias" foi mapeado para `recencia de positivacao global em 60 dias`, conforme visto no exemplo `regra_194`.
3. O segmento "Inativos: os demais" foi implementado como a última regra sem cláusula `quando`, capturando quem não se enquadrou nas regras anteriores (não inadimplente e com mais de 60 dias sem compra).
4. Não foi especificado um `time` no pedido; utilizei um time genérico "time padrao" com "vendedores todos" para que a sintaxe seja válida. Se houver um time específico (ex: televendas, campo), o nome deve ser ajustado.