# informal

## Turno 1 (inicial, 56 s, 15382 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

carteira "padrao":
    clientes carteirafixa("padrao")

parametros "Ativos":
    da carteira("padrao")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

**Premissas:**
1. Como o usuário não especificou o time ou a carteira, assumi a criação de um time "padrao" com todos os vendedores e uma carteira "padrao" vinculada a esse time, que é uma estrutura comum em regras GoBR quando não há especificação.
2. As cláusulas de frequência e critérios de atividade/inatividade foram mantidas conforme o pedido e validadas pelos exemplos.

Perguntas feitas:
- Qual é o nome da carteira e do time que devem ser usados nas regras? (Ex: time "televendas", carteira "televendas") -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Como devo definir o time e a carteira para as regras de Ativos e Inativos? Posso usar `time "padrao": vendedores todos` e `carteira "padrao": clientes carteirafixa("padrao")`? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 29 s, 4924 tokens no maior prompt)

**Usuário:** muda os ativo p 20 dias blz

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

carteira "padrao":
    clientes carteirafixa("padrao")

parametros "Ativos":
    da carteira("padrao")
    quando atividade de 30 dias
    frequencia de 20 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 20 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 20 dias`

**Notas:**
1. **Premissa de Time/Carteira:** Como o usuário não respondeu à pergunta sobre a configuração do time/carteira, mantive a premissa anterior: `time "padrao"` e `carteira "padrao"`.
2. **Atualização de Frequência:** A regra "Ativos" foi atualizada para `frequencia de 20 dias`, conforme solicitado ("muda os ativo p 20 dias").
3. **Inalterado:** A regra "Inativos" permaneceu inalterada, pois o pedido não solicitou mudança nela.

**Verificações:**
- [x] Ativos: {"dias": 20}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] sem o 14

## Turno 3 (alterar, 38 s, 6087 tokens no maior prompt)

**Usuário:** bloqueia quem ta baixado na receita

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

carteira "padrao":
    clientes carteirafixa("padrao")

parametros "Bloqueio baixados na receita":
    da carteira("padrao")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Ativos":
    da carteira("padrao")
    quando atividade de 30 dias
    frequencia de 20 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- incluído: "Bloqueio: situação na receita é baixada"

O que mudou no arquivo:
- "Bloqueio baixados na receita" (parametros): incluída

**Notas:**
1. **Bloqueio:** Adicionada a regra `Bloqueio baixados na receita` com `nao agendar` usando a cláusula `status na receita federal definido como baixada` (encontrada no manual e exemplos).
2. **Ordem:** A regra de bloqueio foi colocada antes das regras de agendamento para garantir que clientes baixados não sejam agendados, mesmo que se enquadrem nos critérios de Ativos ou Inativos (embora a lógica de "inatividade" possa já excluí-los, o bloqueio explícito é mais seguro e segue a prática dos exemplos).
3. **Premissa:** Mantidas as premissas de `time "padrao"` e `carteira "padrao"` por falta de resposta do usuário.

**Verificações:**
- [x] Ativos: {"dias": 20}
- [x] Inativos: {"dias": 28}
- [x] Ativos intacta
- [x] Inativos intacta
