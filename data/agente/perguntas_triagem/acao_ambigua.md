```gobr
version 1.0

time "vendas":
    vendedores todos

parametros "Inadimplentes":
    do time("vendas")
    quando inadimplentes
    nao agendar

parametros "Ativos":
    do time("vendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("vendas")
    frequencia de 28 dias
```

**Observações:**
1. **Correção da cláusula:** A cláusula `recencia de 60 dias` foi substituída por `recencia de positivacao global em 60 dias`, que é a sintaxe correta no GoBR para filtrar clientes com base na última compra (positivação) nos últimos 60 dias, conforme demonstrado nos exemplos e no manual.
2. **Ordem das regras:** Mantida a ordem lógica: bloqueio de inadimplentes, depois ativos (compra recente) e, por fim, a regra "cesta" para os inativos (demais clientes).

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadimplentes": agendar ou não agendar?
Responda numa mensagem só. -> Não agendar os inadimplentes.