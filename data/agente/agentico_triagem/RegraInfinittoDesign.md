```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativo":
    do time("televendas")
    quando atividade de 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando atividade de 90 dias
    frequencia de 7 dias

parametros "Inativo":
    do time("televendas")
    quando inatividade global de 90 dias
    frequencia de 28 dias

parametros "Prospect":
    do time("televendas")
    quando prospects da empresa
    frequencia de 7 dias
```

**Observações e Pontos de Atenção:**

1.  **Ordem das Regras:** A ordem foi ajustada para garantir a lógica de "primeiro que vence".
    *   `Ativo` (até 60 dias) vem primeiro.
    *   `Risco de inatividade` (60-90 dias) vem segundo. Note que a cláusula `atividade de 90 dias` captura quem comprou nos últimos 90 dias. Como a regra de "Ativo" (60 dias) já rodou antes, quem chega nesta regra já foi filtrado (ou seja, não comprou nos últimos 60, mas comprou nos últimos 90).
    *   `Inativo` (>90 dias) vem terceiro.
    *   `Prospect` vem por último. *Atenção:* Se um cliente prospect tiver histórico de compras antigo (ex: há 100 dias), ele cairia em "Inativo" antes de chegar em "Prospect". Se a intenção é que o Ciclo de Vida Prospect sobreponha o histórico de compras, a regra de Prospect deve vir antes das de inatividade. Pelo padrão dos exemplos (regra_197, regra_224), Prospects costumam vir antes das faixas de recência. Vou mover `Prospect` para antes de `Inativo` e `Risco` para seguir o padrão de bloqueio de status, mas manter `Ativo` no topo? Não, o padrão dos exemplos coloca Prospects no início ou no fim? Nos exemplos 197 e 224, Prospects vêm *antes* das faixas de recência. Vou ajustar a ordem para: Ativo, Risco, Prospect, Inativo? Ou Ativo, Risco, Inativo, Prospect?
    *   *Correção de Lógica:* Se um cliente é "Prospect" (nunca comprou), ele não tem recência. Portanto, as cláusulas `atividade de X dias` não se aplicam a ele (ou retornam falso). Então a ordem entre Prospect e as faixas de recência não gera conflito de sobreposição, pois os critérios são mutuamente exclusivos (nunca comprou vs comprou em X dias). A ordem atual está segura.

2.  **Cláusulas Utilizadas:**
    *   `atividade de 60 dias`: Baseado no manual (6.1), "atividade de <<tempo>>" significa "Se o cliente comprou de algum vendedor do grupo no tempo especificado". Isso cobre "pedidos nos últimos 60 dias".
    *   `atividade de 90 dias`: Cobre "pedidos entre 60 e 90 dias" porque a regra de 60 dias já capturou os mais recentes.
    *   `inatividade global de 90 dias`: Baseado no manual (6.1), cobre "sem compra com a empresa toda há pelo menos 90 dias".
    *   `prospects da empresa`: Baseado no manual (6.1), cobre "Clientes que nunca compraram com a empresa".

3.  **Fidelidade ao Pedido:**
    *   "Ativo: ... 14 dias" -> `frequencia de 14 dias`.
    *   "Risco de inatividade: ... 7 dias" -> `frequencia de 7 dias`.
    *   "Inativo: ... 28 dias" -> `frequencia de 28 dias`.
    *   "Prospect: ... 7 dias" -> `frequencia de 7 dias`.

4.  **Premissa Assumida:** Assumi que o time responsável é "televendas", conforme os exemplos fornecidos. Se o pedido original especificasse outro time, deveria ser ajustado. Como não havia especificação de time no `<pedido>`, usei o padrão dos exemplos.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativo; grupo: Ativo, Risco de inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.