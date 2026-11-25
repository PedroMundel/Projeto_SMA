# resposta_com_frequencia_do_grupo

## Turno 1 (inicial, 125 s, 15739 tokens no maior prompt)

**Usuário:** Recorrentes: compra nos últimos 60 dias, 14 dias
Parados: sem compra há mais de 60 dias, 28 dias
Agendar inadimplentes

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Parados":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias

parametros "Inadimplentes":
    do time("televendas")
    quando inadimplentes
    frequencia de 21 dias
```

Inadimplentes: o GoBR não tem cláusula para filtrar clientes por situação financeira/inadimplência.

Divergências entre o pedido e as regras (conferente):
- "Inadimplentes": a regra vem depois de outras que já trataram clientes dela e quase não os pega. Ponha-a antes das faixas de compra.
- "Inadimplentes": A regra inclui clientes que 'nunca compraram', mas o pedido não restringe os inadimplentes a esse grupo, apenas pede para agendar inadimplentes em geral. (pedido: "Inadimplentes: de 21 em 21 dias")

Pontos de atenção na modelagem:
- A correção pedida pelo conferente não passou no validador; esta é a última versão que passou.
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadimplentes": de quantos em quantos dias agendar?
Responda numa mensagem só. -> Os inadimplentes de 21 em 21 dias.

**Verificações:**
- [x] Recorrentes: {"dias": 14}
- [x] Parados: {"dias": 28}
- [x] Inadimplentes: {"dias": 21}
