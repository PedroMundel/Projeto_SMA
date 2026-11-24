# completa_depois

## Turno 1 (inicial, 56 s, 6119 tokens no maior prompt)

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

## Turno 2 (alterar, 31 s, 4999 tokens no maior prompt)

**Usuário:** Os inativos são a cada 21 dias.

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
    frequencia de 21 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 30 dias" para "Inativos: sem compra há mais de 30 dias, 21 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `nao agendar`, entrou `frequencia de 21 dias`

**Notas e Premissas:**
1.  **Ação para Inativos:** Mantida a premissa anterior de `nao agendar` alterada para `frequencia de 21 dias` conforme a nova instrução do usuário ("Os inativos são a cada 21 dias").
2.  **Critério de Inatividade:** Utilizada a cláusula `inatividade de 30 dias` para refletir "sem compra há mais de 30 dias".
3.  **Ordem das Regras:** A regra "Ativos" vem primeiro para capturar quem comprou nos últimos 30 dias. A regra "Inativos" captura quem não se encaixa na anterior (ou seja, não comprou nos últimos 30 dias) e aplica a frequência de 21 dias.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 21}
- [x] Ativos intacta
- [x] até 0 perguntas
