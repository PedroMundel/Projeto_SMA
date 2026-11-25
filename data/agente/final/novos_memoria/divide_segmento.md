# divide_segmento

## Turno 1 (inicial, 27 s, 4883 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Inativos":
    do time("televendas")
    quando nao tem venda em 60 dias
    frequencia de 28 dias

parametros "Ativos":
    do time("televendas")
    quando tem venda em 60 dias
    frequencia de 14 dias
```

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (alterar, 140 s, 22198 tokens no maior prompt)

**Usuário:** Separe os inativos em dois: sem compra entre 60 e 120 dias, a cada 21 dias, e sem compra há mais de 120 dias, a cada 45 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda em 60 dias
    frequencia de 14 dias

parametros "Inativos 60-120 dias":
    do time("televendas")
    quando recencia de positivacao global entre 61 dias e 120 dias
    frequencia de 21 dias

parametros "Inativos +120 dias":
    do time("televendas")
    quando fora da recencia de positivacao global em 120 dias
    frequencia de 45 dias
```

Mudança no pedido:
- removido: "Inativos: sem compra há mais de 60 dias, 28 dias"
- incluído: "Inativos: sem compra entre 60 e 120 dias, 21 dias"
- incluído: "Inativos: sem compra há mais de 120 dias, 45 dias"

O que mudou no arquivo:
- "Inativos 60-120 dias" (parametros): incluída
- "Inativos +120 dias" (parametros): incluída
- "Inativos" (parametros): removida

O GoBR não tem cláusula para "inatividade entre 60 e 120 dias" exata; usei `recencia de positivacao global entre 61 dias e 120 dias` baseado em exemplos de faixas de recência. A lógica de ordem (Ativos primeiro, depois faixas de inatividade) está preservada.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativos 60-120 dias, Inativos +120 dias; grupo: Ativos); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

**Verificações:**
- [x] Ativos intacta
- [x] sem o 28
- [x] com o 120
- [x] com o 21
- [x] com o 45
