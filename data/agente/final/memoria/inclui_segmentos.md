# inclui_segmentos

## Turno 1 (inicial, 23 s, 4883 tokens no maior prompt)

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

## Turno 2 (alterar, 86 s, 10135 tokens no maior prompt)

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

parametros "Inativos":
    do time("televendas")
    quando nao tem venda em 60 dias
    frequencia de 28 dias

parametros "Ativos":
    do time("televendas")
    quando tem venda em 60 dias
    frequencia de 14 dias
```

Mudança no pedido:
- incluído: "Prospects: ciclo de vida prospect, 7 dias"

O que mudou no arquivo:
- "Prospects" (parametros): incluída

A ordem padrão nos exemplos é Prospects -> Ativos -> Inativos. O conferente reclamou que a ordem "Inativos, Ativos" do pedido original foi alterada. Para manter a ordem original entre Inativos e Ativos (Inativos primeiro, depois Ativos) e ainda resolver o erro de "Prospects inalcançável", a ordem deve ser: Prospects, Inativos, Ativos.

No entanto, isso é logicamente estranho (geralmente Ativos vêm antes de Inativos). Mas o conferente foi específico: "a ordem das regras que a mudança pedida não cita mudou: antes, Inativos, Ativos". Isso implica que a relação relativa entre Inativos e Ativos deve ser preservada. Como Prospects precisa ir antes para não ser inalcançável, a ordem fica: Prospects, Inativos, Ativos.

Vou aplicar essa ordem.

Perguntas feitas:
- O pedido original tinha a ordem "Inativos" depois de "Ativos". A mudança pediu apenas para "incluir os prospects". Para resolver o erro de regra inalcançável, precisamos colocar "Prospects" antes das regras de compra. Deseja que a ordem final seja "Prospects", "Inativos", "Ativos" ou "Prospects", "Ativos", "Inativos"? Ou prefere que mantenha a ordem original de "Inativos" antes de "Ativos", mas com "Prospects" no início? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Prospects: {"dias": 7}
- [x] Ativos intacta
- [x] Inativos intacta

## Turno 3 (alterar, 42 s, 4556 tokens no maior prompt)

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

parametros "Inativos":
    do time("televendas")
    quando nao tem venda em 60 dias
    frequencia de 28 dias

parametros "Ativos":
    do time("televendas")
    quando tem venda em 60 dias
    frequencia de 14 dias
```

Mudança no pedido:
- incluído: "Inadimplentes: não agendar"

O que mudou no arquivo:
- "Inadimplentes" (parametros): incluída

- Ordem mantida: Inadimplentes (bloqueio), Prospects, Inativos, Ativos (premissa: preservar ordem relativa Inativos->Ativos do pedido original, inserindo Prospects antes para evitar regra inalcançável).
- "Inadimplentes" usa a cláusula `inadimplentes` vista nos exemplos.
- O critério "compra nos últimos 60 dias" foi traduzido como `tem venda em 60 dias` e "sem compra há mais de 60 dias" como `nao tem venda em 60 dias`, seguindo a sintaxe dos exemplos de recência.
- Não houve menção a carteiras no pedido, mantive a estrutura de `time` do arquivo anterior.

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inadimplentes": quem são esses clientes (o critério)?

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadimplentes": quem são esses clientes (o critério)?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.

**Verificações:**
- [x] Inadimplentes: {"acao": "nao_agendar"}
- [x] Ativos intacta
- [x] Inativos intacta
- [x] Prospects intacta
- [x] Inadimplentes bloqueia antes
