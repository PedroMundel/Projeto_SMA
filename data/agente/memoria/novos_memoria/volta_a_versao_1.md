# volta_a_versao_1

## Turno 1 (inicial, 54 s, 15382 tokens no maior prompt)

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

## Turno 2 (alterar, 33 s, 5005 tokens no maior prompt)

**Usuário:** Ativos a cada 9 dias.

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
    frequencia de 9 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 9 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 9 dias`

**Notas:**
1. **Premissa de Time/Carteira:** Como o usuário não respondeu à pergunta anterior, mantive a premissa de usar `time "padrao"` e `carteira "padrao"` conforme a versão 1.
2. **Mudança Aplicada:** A frequência da regra "Ativos" foi alterada de `14 dias` para `9 dias`, conforme solicitado na mudança.
3. **Cláusulas:** Utilizei `atividade de 30 dias` para o segmento "Ativos" (compra nos últimos 30 dias) e `inatividade de 30 dias` para o segmento "Inativos" (sem compra há mais de 30 dias), baseando-me na estrutura dos exemplos e no manual (seção 6.1).

**Verificações:**
- [x] Ativos: {"dias": 9}
- [x] Inativos intacta

## Turno 3 (alterar, 30 s, 5289 tokens no maior prompt)

**Usuário:** E inativos a cada 40.

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
    frequencia de 9 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 40 dias
```

Mudança no pedido:
- de "Inativos: sem compra há mais de 30 dias, 28 dias" para "Inativos: sem compra há mais de 30 dias, 40 dias"

O que mudou no arquivo:
- "Inativos" (parametros): saiu `frequencia de 28 dias`, entrou `frequencia de 40 dias`

**Notas:**
1. **Premissa de Time/Carteira:** Mantida a premissa da versão anterior (`time "padrao"`, `carteira "padrao"`) por falta de resposta do usuário.
2. **Mudança Aplicada:** A frequência da regra "Inativos" foi alterada de `28 dias` para `40 dias`, conforme solicitado ("E inativos a cada 40").
3. **Cláusulas:** Mantidas as cláusulas `atividade de 30 dias` e `inatividade de 30 dias` baseadas na versão anterior e nos exemplos do manual (seção 6.1).

**Verificações:**
- [x] Inativos: {"dias": 40}
- [x] Ativos intacta

## Turno 4 (desfazer, 2 s, 1156 tokens no maior prompt)

**Usuário:** Volta tudo para a versão 1.

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

Voltei à versão 1, com o pedido dela:
- Ativos: compra nos últimos 30 dias, 14 dias
- Inativos: sem compra há mais de 30 dias, 28 dias

**Verificações:**
- [x] arquivo do turno 1
- [x] arquivo difere do turno 3
