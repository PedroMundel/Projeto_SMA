# conversa_longa

## Turno 1 (inicial, 22 s, 4770 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 24 s, 4833 tokens no maior prompt)

**Usuário:** Troque os ativos para 10 dias.

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 60 dias, 14 dias" para "Ativos: compra nos últimos 60 dias, 10 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 10 dias`

**Verificações:**
- [x] Ativos: {"dias": 10}
- [x] Inativos intacta

## Turno 3 (alterar, 25 s, 5307 tokens no maior prompt)

**Usuário:** Os inativos passam para 35 dias.

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 35 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 60 dias, 28 dias" para "Inativos: sem compra há mais de 60 dias, 35 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 35 dias`

**Verificações:**
- [x] Inativos: {"dias": 35}
- [x] Ativos intacta

## Turno 4 (alterar, 28 s, 4531 tokens no maior prompt)

**Usuário:** Inclua prospects (ciclo de vida prospect) a cada 7 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 35 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

Mudança no pedido:
- incluído: "Prospects: ciclo de vida prospect, 7 dias"

O que mudou no arquivo:
- "Prospects" (parametros): incluída

**Verificações:**
- [x] Prospects: {"dias": 7}
- [x] Ativos intacta
- [x] Inativos intacta

## Turno 5 (alterar, 33 s, 4374 tokens no maior prompt)

**Usuário:** Não agende quem está inadimplente.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 35 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

Mudança no pedido:
- incluído: "Inadimplentes: não agendar"

O que mudou no arquivo:
- "Inadimplentes" (parametros): incluída

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inadimplentes": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadimplentes": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [x] Ativos intacta
- [x] Inativos intacta
- [x] Prospects intacta
- [x] Inadimplentes bloqueia antes

## Turno 6 (alterar, 40 s, 5264 tokens no maior prompt)

**Usuário:** Volte os ativos para 12 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 12 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 35 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 60 dias, 10 dias" para "Ativos: compra nos últimos 60 dias, 12 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 10 dias`, entrou `frequencia de 12 dias`

**Notas:**
- "Inadimplentes": o GoBR não tem cláusula para definir quem é inadimplente além de `quando inadimplentes` (usada no arquivo anterior). Mantive essa cláusula, assumindo que ela está disponível no ambiente ou é um filtro customizado aceito pelo validador, pois o manual não detalha "inadimplentes" especificamente, mas o exemplo anterior a usou com sucesso. Se `inadimplentes` não for uma cláusula válida, esta regra precisaria de um critério alternativo (ex: `inativos para a empresa` ou similar) ou ser removida.
- A ordem das regras mantém o bloqueio (`nao agendar`) primeiro, seguido pelas faixas de frequência.
- Todos os números do pedido (60, 12, 35, 7) estão presentes nas cláusulas correspondentes.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inadimplentes": quem são esses clientes (o critério)?

**Verificações:**
- [x] Ativos: {"dias": 12}
- [x] Inativos intacta
- [x] Prospects intacta

## Turno 7 (duvida, 10 s, 2303 tokens no maior prompt)

**Usuário:** Qual era a frequência dos ativos no meu primeiro pedido, e qual é a de agora?

**Agente:**

No primeiro pedido (versão 1), a frequência dos ativos era de 14 dias.
Na versão atual (versão 6), a frequência dos ativos é de 12 dias.

**Verificações:**
- [x] arquivo do turno 6
- [x] resposta tem 14
- [x] resposta tem 12
