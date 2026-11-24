# muda_criterio

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

## Turno 2 (alterar, 32 s, 5451 tokens no maior prompt)

**Usuário:** O corte entre ativo e inativo passa a ser de 45 dias sem compra, as frequências continuam.

**Agente:**

```gobr
version 1.0

time "padrao":
    vendedores todos

carteira "padrao":
    clientes carteirafixa("padrao")

parametros "Ativos":
    da carteira("padrao")
    quando atividade de 45 dias
    frequencia de 14 dias

parametros "Inativos":
    da carteira("padrao")
    quando inatividade de 45 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 45 dias, 14 dias"
- de "Inativos: sem compra há mais de 30 dias, 28 dias" para "Inativos: sem compra há mais de 45 dias, 28 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `atividade de 30 dias`, entrou `atividade de 45 dias`
- "Inativos" (parametros): saiu `inatividade de 30 dias`, entrou `inatividade de 45 dias`

**Notas:**
1. **Premissa de Time/Carteira:** Como o usuário não respondeu à pergunta anterior, mantive a premissa de usar `time "padrao"` e `carteira "padrao"` conforme a versão 1.
2. **Atualização de Critérios:** Os critérios de recência foram alterados de 30 para 45 dias em ambas as regras, conforme solicitado na mudança.
3. **Cláusulas Utilizadas:** Utilizei `atividade de 45 dias` para definir clientes com compra recente (Ativos) e `inatividade de 45 dias` para definir clientes sem compra há mais de 45 dias (Inativos), baseando-me na sintaxe do arquivo anterior e nas opções do manual (seção 6.1).

**Verificações:**
- [x] Ativos: {"dias": 14, "numero": 45}
- [x] Inativos: {"dias": 28}
- [x] sem o 30
