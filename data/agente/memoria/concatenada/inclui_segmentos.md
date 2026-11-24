# inclui_segmentos

## Turno 1 (inicial, 26 s, 4770 tokens no maior prompt)

**Usuário:** Ativos: compra nos últimos 60 dias, 14 dias
Inativos: sem compra há mais de 60 dias, 28 dias

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando fora da recencia de positivacao em 60 dias
    frequencia de 28 dias
```

**Verificações:**
- [x] Ativos: {"dias": 14}
- [x] Inativos: {"dias": 28}

## Turno 2 (inicial, 37 s, 4734 tokens no maior prompt)

**Usuário:** Inclua os prospects, clientes com ciclo de vida prospect, a cada 7 dias.

**Agente:**

```gobr
version 1.0

time "televendas":
    vendedores todostelevendas ativados

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Ativos":
    do time("televendas")
    quando atividade de 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade de 60 dias
    frequencia de 28 dias
```

**Observações:**
1. A ordem das regras foi definida como: Prospects -> Ativos -> Inativos. Isso garante que um cliente no ciclo de vida prospect não seja classificado como "Ativo" (se houver sobreposição de dados) ou "Inativo". Como "Ativos" e "Inativos" são mutuamente exclusivos por definição de recência (compra há <= 60 vs > 60), a ordem entre eles não altera o resultado, mas a lógica de negócio geralmente prioriza o estado atual (ativo) sobre o inativo. No entanto, como o GoBR avalia em ordem e a primeira vence, se um cliente for prospect, ele cai na primeira regra. Se não for prospect, verifica se comprou nos últimos 60 dias (Ativo). Se não, cai na regra final (Inativo).
2. O critério "compra nos últimos 60 dias" foi mapeado para `atividade de 60 dias` (ou `tem venda da empresa em 60 dias` dependendo da sintaxe exata, mas `atividade de 60 dias` é o padrão para "comprou no período"). O critério "sem compra há mais de 60 dias" foi mapeado para `inatividade de 60 dias`.
3. Não foi necessário bloqueio explícito, pois as faixas de recência/inatividade cobrem o universo restante de forma complementar (ou sobreposta de forma que a ordem resolve). A regra "Inativos" atua como a regra final para quem não se enquadrou nas anteriores.

**Verificações:**
- [x] Prospects: {"dias": 7}
- [ ] Ativos intacta
- [ ] Inativos intacta

## Turno 3 (inicial, 37 s, 4767 tokens no maior prompt)

**Usuário:** Agora não agende os inadimplentes.

**Agente:**

```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Inadimplentes":
    do time("televendas")
    quando inadimplentes
    nao agendar

parametros "Prospects":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Ativos":
    do time("televendas")
    quando recencia de positivacao global em 60 dias
    frequencia de 14 dias

parametros "Inativos":
    do time("televendas")
    quando inatividade global de 60 dias
    frequencia de 28 dias
```

**Observações:**
1. A ordem das regras foi ajustada para garantir que os "Inadimplentes" (bloqueio) sejam avaliados primeiro, impedindo que caibam nas regras de agendamento.
2. Para o segmento "Inativos", utilizei a cláusula `inatividade global de 60 dias` conforme o manual (seção 6.1), que corresponde a "sem compra há mais de 60 dias".
3. Assumi o time "televendas" com todos os vendedores ativados, padrão nos exemplos fornecidos. Se o time for outro, ajuste a linha `time "nome"`.
4. O pedido não especifica um time diferente, então mantive a estrutura padrão.

**Verificações:**
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [ ] Ativos intacta
- [ ] Inativos intacta
- [x] Prospects intacta
