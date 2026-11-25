# duvida_de_cascata

## Turno 1 (inicial, 149 s, 12682 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Risco: última compra entre 30 e 60 dias, 7 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 30 dias
    frequencia de 14 dias

parametros "Risco":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 7 dias

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Inativos":
    do time("televendas")
    frequencia de 28 dias
```

Notas:
- Adicionei a regra "Prospects" para excluir clientes que nunca compraram da regra "Inativos", conforme apontado pelo conferente.
- Assumi frequência de 7 dias para Prospects (premissa baseada no exemplo 194).
- A ordem das regras garante a exclusividade: Ativos (<=30d), Risco (30-60d), Prospects (nunca comprou), Inativos (>60d e já comprou).

Wait, if I put Prospects before Inativos, Inativos will catch everyone who is NOT Active, NOT Risk, and NOT Prospect.
Active: <= 30 days.
Risk: <= 60 days (so 30-60 days effectively).
Prospect: Never bought.
Inativos: Everyone else. Who is everyone else? People who haven't bought in > 60 days AND have bought before. This matches the request perfectly.

One detail: The prompt says "Inativos: sem compra há mais de 60 dias".
If I use `recencia de positivacao em 60 dias` for Risco, it catches <= 60 days.
So Inativos catches > 60 days.
This logic holds.

Let's verify the "Risco" definition: "última compra entre 30 e 60 dias".
Rule 1: `recencia de positivacao em 30 dias` -> Catches <= 30.
Rule 2: `recencia de positivacao em 60 dias` -> Catches <= 60. Since <= 30 is already taken, this catches (30, 60].
Rule 3: `no ciclo de vida prospect` ->…

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

Perguntas feitas:
- O segmento "Inativos" deve excluir os clientes que nunca compraram (Prospects)? Ou seja, Inativos refere-se apenas a clientes que já compraram, mas não compram há mais de 60 dias? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Para corrigir a regra de Inativos (que não deve incluir clientes que nunca compraram), preciso criar uma regra para Prospects. Qual a frequência de agendamento para Prospects? (Ex: 7 dias, 14 dias) -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Risco: {"dias": 7}
- [x] Inativos: {"dias": 28}

## Turno 2 (duvida, 10 s, 1832 tokens no maior prompt)

**Usuário:** Um cliente que comprou há 40 dias cai em qual regra?

**Agente:**

O cliente cai na regra "Risco".

Ele comprou há 40 dias, o que significa que está há menos de 60 dias desde a última compra (saindo de "Inativos") e mais de 30 dias (saindo de "Ativos"). A regra "Risco" captura clientes que compraram nos últimos 60 dias, mas estão há mais de 30 dias sem comprar.

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem Risco

## Turno 3 (duvida, 10 s, 2492 tokens no maior prompt)

**Usuário:** E um que está sem comprar há 100 dias, é agendado de quanto em quanto tempo?

**Agente:**

O cliente cai na regra "Inativos", pois está há mais de 60 dias sem comprar. A frequência de agendamento para essa regra é de 28 dias.

**Verificações:**
- [x] arquivo do turno 1
- [x] resposta tem 28
