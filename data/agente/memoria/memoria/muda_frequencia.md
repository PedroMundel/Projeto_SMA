# muda_frequencia

## Turno 1 (inicial, 61 s, 15382 tokens no maior prompt)

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

## Turno 2 (alterar, 34 s, 4990 tokens no maior prompt)

**Usuário:** Troque os ativos para 15 dias.

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
    frequencia de 15 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 15 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 15 dias`

**Notas:**
1. **Premissa de Time/Carteira:** Como o usuário não respondeu à pergunta sobre o nome do time/carteira, mantive a premissa anterior de usar `time "padrao"` e `carteira "padrao"`.
2. **Alteração Aplicada:** A frequência da regra "Ativos" foi alterada de `14 dias` para `15 dias`, conforme solicitado na mudança. O critério de recência (30 dias) e a regra "Inativos" permaneceram inalterados.

**Verificações:**
- [x] Ativos: {"dias": 15}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] sem o 14

## Turno 3 (duvida, 9 s, 1828 tokens no maior prompt)

**Usuário:** E os inativos, ficaram a cada quantos dias?

**Agente:**

Os inativos continuam com frequência de 28 dias.
Isso porque a última alteração (versão 2) modificou apenas a regra dos "Ativos" para 15 dias.
A regra dos "Inativos" não foi alterada e permanece com frequência de 28 dias.
Portanto, a configuração atual é: Ativos a cada 15 dias e Inativos a cada 28 dias.

**Verificações:**
- [x] arquivo do turno 2
- [x] resposta tem 28
