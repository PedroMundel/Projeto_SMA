# completa_depois

## Turno 1 (inicial, 55 s, 6119 tokens no maior prompt)

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
    nao agendar
```

**Notas e Premissas:**

1.  **Ação para Inativos:** Como o usuário não respondeu à pergunta sobre a ação para o segmento "Inativos", segui a premissa mais provável baseada nos exemplos do manual (ex: `regra_070`), onde clientes inativos são frequentemente bloqueados (`nao agendar`) para evitar desperdício de esforço comercial.
2.  **Critério de Inatividade:** Ajustei a cláusula para `inatividade de 30 dias` para refletir exatamente o critério "sem compra há mais de 30 dias" mencionado no pedido, em vez do status genérico `inativos para o vendedor`.
3.  **Ambiguidade:** O pedido não especificou ação para inativos. A escolha por `nao agendar` é uma premissa comercial padrão para inativos, mas pode precisar de ajuste se a estratégia for reativa (agendar com frequência baixa).

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inativos": agendar ou não agendar?
- Inativos: Bloqueio depois de regras de frequência: clientes já parametrizados por "Ativos" não serão bloqueados por esta regra.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": agendar ou não agendar?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Para o segmento "Inativos" (sem compra há mais de 30 dias), qual deve ser a ação? Agendar com qual frequência ou não agendar? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 14}

## Turno 2 (inicial, 20 s, 3900 tokens no maior prompt)

**Usuário:** Os inativos são a cada 21 dias.

**Agente:**

```gobr
version 1.0

time "empresa toda":
    vendedores todos

parametros "Inativos: 21 dias":
    da carteira("empresa toda")
    quando inativos para o vendedor
    frequencia de 21 dias
```

**Notas:**
1. **Segmento genérico:** Como o pedido não especificou uma carteira ou time, assumi a carteira fixa padrão e todos os vendedores da empresa, seguindo o padrão dos exemplos fornecidos.
2. **Critério de Inatividade:** Utilizei a cláusula `inativos para o vendedor`, que é o filtro padrão para definir inatividade baseada no histórico do vendedor, conforme o manual (seção 6.1).
3. **Frequência:** Aplicada a frequência de 21 dias conforme solicitado.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 21}
- [ ] Ativos intacta
- [ ] até 0 perguntas
