# muda_frequencia

## Turno 1 (inicial, 28 s, 4750 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 30 dias, 14 dias
Inativos: sem compra há mais de 30 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 28 s, 4743 tokens no maior prompt)

**Usuário:** Troque os ativos para 15 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando atividade de 30 dias
    frequencia de 15 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 30 dias
    frequencia de 28 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 30 dias, 14 dias" para "Ativos: compra nos últimos 30 dias, 15 dias"

O que mudou no arquivo:
- "Ativos" (parametros): saiu `frequencia de 14 dias`, entrou `frequencia de 15 dias`

**Verificações:**
- [x] Ativos: {"dias": 15}
- [x] Inativos: {"dias": 28}
- [x] Inativos intacta
- [x] sem o 14

## Turno 3 (duvida, 9 s, 1683 tokens no maior prompt)

**Usuário:** E os inativos, ficaram a cada quantos dias?

**Agente:**

Os inativos continuam com frequência de 28 dias.
Isso está definido na regra "Inativos" do arquivo atual (versão 2).
A conversa mostra que apenas a frequência dos "Ativos" foi alterada para 15 dias.
A regra dos inativos não foi modificada desde a versão 1.
Portanto, o agendamento para inativos permanece a cada 28 dias.

**Verificações:**
- [x] arquivo do turno 2
- [x] resposta tem 28
