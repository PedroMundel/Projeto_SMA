# lembra_resposta

## Turno 1 (inicial, 86 s, 12889 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

parametros "Ativos":
    do time("padrao")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Os inativos a cada 28 dias.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 19 s, 2857 tokens no maior prompt)

**Usuário:** Mude os ativos para 7 dias.

**Agente:**

```gobr
version 1.0

time "empresa toda":
    vendedores todos

carteira "empresa toda":
    clientes carteirafixa("empresa toda")

parametros "Ativos: Frequência de 7 dias":
    da carteira("empresa toda")
    quando ativos para o vendedor
    frequencia de 7 dias
```

**Notas e Premissas:**
1.  **Segmento "Ativos":** Como o pedido não especificou um tempo de recência (ex: "compra nos últimos 30 dias"), assumi a cláusula padrão `quando ativos para o vendedor` (presente no exemplo 172), que identifica clientes com atividade recente.
2.  **Ação:** O pedido pediu para mudar ativos para 7 dias. A regra aplica `frequencia de 7 dias` ao segmento de ativos.
3.  **Fidelidade:** O valor "7 dias" foi mantido integralmente. Não foram aplicados bloqueios pois nenhum foi solicitado no trecho fornecido.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Ativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 7}
- [ ] Inativos: {"dias": 28}
- [ ] Inativos intacta
- [ ] até 0 perguntas
