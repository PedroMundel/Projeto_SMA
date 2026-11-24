# volta_a_versao_1

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

## Turno 2 (inicial, 22 s, 3911 tokens no maior prompt)

**Usuário:** Ativos a cada 9 dias.

**Agente:**

```gobr
version 1.0

time "todos":
    vendedores todos ativados

parametros "Ativos":
    do time("todos")
    quando ativos
    frequencia de 9 dias
```

**Notas:**
1. **Segmento Genérico:** Como o pedido não especificou um time (ex: televendas, campo), assumi o time "todos" (vendedores todos ativados), que é o padrão em regras gerais.
2. **Critério "Ativos":** O pedido não definiu um critério de recência específico (ex: "compra nos últimos 30 dias"). Utilizei o filtro `ativos` (clientes considerados ativos pelos critérios padrão do sistema), conforme exemplo 172 e 060.
3. **Ação:** A frequência de 9 dias foi aplicada diretamente.
4. **O que ficou de fora:** O pedido não especificou o time de vendedores; assumiu-se "todos". Não há menção a bloqueios (inadimplentes, filiais), então a regra aplica-se a todos os ativos.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Ativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Ativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 9}
- [ ] Inativos intacta

## Turno 3 (inicial, 23 s, 5735 tokens no maior prompt)

**Usuário:** E inativos a cada 40.

**Agente:**

```gobr
version 1.0

time "empresa toda":
    vendedores todos

carteira "empresa toda":
    clientes carteirafixa("empresa toda")

parametros "Inativos a cada 40 dias":
    da carteira("empresa toda")
    quando inativos para o vendedor
    frequencia de 40 dias
```

**Notas:**
1. **Critério de Inatividade:** O pedido não especificou o tempo de inatividade (ex: "inativos há 90 dias"). Assumi a cláusula padrão `inativos para o vendedor` (que usa o critério global do sistema). Se houver um tempo específico, a cláusula seria `inatividade de X dias`.
2. **Segmento:** Como não foi definido um time ou carteira específica, assumi "empresa toda" e "carteira fixa" como padrão.
3. **Conflito Potencial:** Se existirem regras anteriores que bloqueiem ou tratem inativos com outra frequência, esta regra só aplicará aos inativos que sobrarem.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inativos": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inativos": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Inativos: {"dias": 40}
- [ ] Ativos intacta

## Turno 4 (inicial, 57 s, 18237 tokens no maior prompt)

**Usuário:** Volta tudo para a versão 1.

**Agente:**

```gobr
version 1.0
```

Premissa assumida: Como o pedido "Volta tudo para a versão 1" não especifica segmentos, critérios ou frequências, e não houve resposta do usuário para esclarecimento, assumi que não há regras de negócio para implementar neste momento. O arquivo contém apenas a versão obrigatória, sem regras `parametros`, pois nenhuma foi solicitada. Se houver regras desejadas, por favor, envie o pedido detalhado.

Erros que ficaram depois de 3 entregas:
- O arquivo não tem nenhuma regra `parametros`.

Pontos de atenção na modelagem:
- A triagem não achou segmentos no pedido; o pedido não foi conferido segmento a segmento.
- Números do pedido que ficaram de fora do GoBR (ver notas): 1.

Perguntas feitas:
- Qual é o pedido de negócio completo (segmentos, critérios e frequências) que você deseja transformar em regras GoBR? O texto "Volta tudo para a versão 1" não contém informações suficientes para definir as regras. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [ ] arquivo do turno 1
- [ ] arquivo difere do turno 3
