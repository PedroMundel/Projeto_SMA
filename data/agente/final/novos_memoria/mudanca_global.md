# mudanca_global

## Turno 1 (inicial, 112 s, 14663 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 45 dias, 14 dias
Inativos: sem compra há mais de 45 dias, 28 dias

**Agente:**

<tool_call>
<function=buscar_exemplos>
<parameter=consulta>
regra de agendamento ativos inativos sem bloqueio previo
</parameter>
</function>
</tool_call>

Erros que ficaram depois de 3 entregas:
- A resposta não trouxe um bloco ```gobr com o arquivo.

**Verificações:**
- [ ] Ativos: {"dias": 14}
- [ ] Inativos: {"dias": 28}

## Turno 2 (alterar, 60 s, 7354 tokens no maior prompt)

**Usuário:** Quero todos os segmentos com a mesma frequência, a cada 10 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Ativos":
    do time("televendas")
    quando tem venda da empresa em 45 dias
    frequencia de 10 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 45 dias
    frequencia de 10 dias
```

Mudança no pedido:
- de "Ativos: compra nos últimos 45 dias, 14 dias" para "Ativos: compra nos últimos 45 dias, 10 dias"
- de "Inativos: sem compra há mais de 45 dias, 28 dias" para "Inativos: sem compra há mais de 45 dias, 10 dias"

O erro "inalcançável" ocorre porque a regra "Ativos" usa `tem venda da empresa em 45 dias`, que é exatamente a mesma condição da regra de bloqueio anterior. Como o GoBR processa em ordem e a primeira regra que se aplica vence, nenhum cliente chega à regra "Ativos", pois todos que têm venda nos últimos 45 dias já foram "pegos" pelo `nao agendar`.

Para corrigir, a regra "Ativos" deve capturar quem comprou nos últimos 45 dias, mas que **não** está no bloqueio. Como o bloqueio é "compra nos últimos 45 dias", não há como ter uma regra de agendamento para "ativos" (compra recente) se o bloqueio também é "compra recente".

Analisando o pedido:
- Ativos: compra nos últimos 45 dias -> Agendar
- Inativos: sem compra há mais de 45 dias -> Agendar

O erro anterior foi criar um bloqueio para "compra nos últimos 45 dias" e depois tentar agendar "ativos" (que também são compra nos últimos 45 dias). Isso é contraditório. Se o pedido manda agendar os ativos, não deve haver bloqueio para eles. O bloqueio anterior foi uma interpretação equivocada de que "ativos" precisavam ser separados de um bloqueio genérico, mas o pedido não pede bloqueio.

No entanto, olhando os exemplos, muitas vezes há um bloq…

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Ativos; grupo: Inativos); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.

**Verificações:**
- [x] Ativos: {"dias": 10, "numero": 45}
- [x] Inativos: {"dias": 10}
- [x] sem o 14
- [x] sem o 28
