# tira_e_poe_de_volta

## Turno 1 (inicial, 43 s, 5715 tokens no maior prompt)

**Usuário:** Novos: clientes com ciclo de vida prospect, 5 dias
Recorrentes: compra nos últimos 90 dias, 20 dias
Restantes: 45 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Novos":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 5 dias

parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 20 dias

parametros "Restantes":
    do time("televendas")
    frequencia de 45 dias
```

**Premissas e Pontos Falhos:**
1. **Ordem das Regras:** A regra "Novos" vem antes de "Recorrentes" e "Restantes". Como "Recorrentes" usa `recencia de positivacao global em 90 dias`, ela também capturaria clientes "Novos" se estes tivessem alguma compra (o que contradiz a definição de prospect, mas a ordem garante que o prospect seja identificado primeiro). A regra "Restantes" é a "catch-all" final.
2. **Critério "Restantes":** O pedido não definiu um critério explícito para "Restantes", apenas a frequência. A regra GoBR correspondente é uma cláusula sem `quando` (ou com `quando` vazio/implícito), que captura todos os clientes que não se encaixaram nas regras anteriores.
3. **Segmentos sobrepostos:** Não há sobreposição lógica entre "Prospect" (nunca comprou) e "Compra nos últimos 90 dias" (já comprou), desde que a definição de prospect seja estrita de "sem compras". Se houver clientes prospect com compras recentes (inconsistência de dados), a ordem das regras resolve.
4. **Fidelidade:** Todos os números (5, 90, 20, 45) estão presentes. A ação "agendar" foi convertida para `frequencia de X dias`. O time foi aplicado conforme a premissa.

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Novos: {"dias": 5}
- [x] Recorrentes: {"dias": 20}
- [x] Restantes: {"dias": 45}

## Turno 2 (alterar, 32 s, 5665 tokens no maior prompt)

**Usuário:** Pode remover os novos.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 20 dias

parametros "Restantes":
    do time("televendas")
    frequencia de 45 dias
```

Mudança no pedido:
- removido: "Novos: clientes com ciclo de vida prospect, 5 dias"

O que mudou no arquivo:
- "Novos" (parametros): removida

**Verificações:**
- [x] sem regra Novos
- [x] Recorrentes intacta
- [x] Restantes intacta
- [x] sem o 5

## Turno 3 (desfazer, 2 s, 1028 tokens no maior prompt)

**Usuário:** Pensando bem, desfaz isso.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Novos":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 5 dias

parametros "Recorrentes":
    do time("televendas")
    quando recencia de positivacao global em 90 dias
    frequencia de 20 dias

parametros "Restantes":
    do time("televendas")
    frequencia de 45 dias
```

Voltei à versão 1, com o pedido dela:
- Novos: clientes com ciclo de vida prospect, 5 dias
- Recorrentes: compra nos últimos 90 dias, 20 dias
- Restantes: 45 dias

**Verificações:**
- [x] arquivo do turno 1
- [x] arquivo difere do turno 2
