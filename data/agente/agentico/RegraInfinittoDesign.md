```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Prospect":
    do time("televendas")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

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
```

**O que ficou de fora / Premissas / Pontos falhos:**

1.  **Ordem de Execução (Lógica de Faixas):** O pedido define "Ativo" como compras nos últimos 60 dias e "Risco" como entre 60 e 90 dias. No GoBR, a cláusula `atividade de 90 dias` seleciona quem comprou nos últimos 90 dias (incluindo os últimos 60). Para que a regra "Risco" capture apenas o intervalo (60, 90], ela deve vir **antes** da regra "Ativo" no arquivo, ou a regra "Ativo" deve ser mais restritiva. Como o GoBR avalia em ordem e a primeira vence, coloquei "Ativo" antes. Se um cliente comprou há 30 dias, ele entra em "Ativo". Se comprou há 70 dias, ele não entra em "Ativo" (se eu usasse uma lógica de exclusão, mas não há cláusula `quando não atividade de 60 dias` explícita simples sem sobreposição complexa).
    *   *Correção de Lógica:* Analisando os exemplos (regra_197, regra_224), a prática comum para faixas de recência é usar `recencia de positivacao global em X dias`. O exemplo usa `recencia de positivacao global em 60 dias` para Ativos e `recencia de positivacao global em 90 dias` para Risco. Isso implica que a regra de 60 dias captura os mais recentes e a de 90 dias captura os restantes dentro de 90? Não, geralmente `recencia em X` captura todos até X.
    *   *Reavaliando com base nos exemplos:* Nos exemplos, `Clientes Ativos` usa `recencia de positivacao global em 60 dias` e `Risco de Inatividade` usa `recencia de positivacao global em 90 dias`. Se a regra de Ativos vem primeiro, ela pega quem comprou em 60 dias. Quem comprou em 70 dias não pega em Ativos. A regra de Risco (90 dias) pega quem comprou em 70 dias. Isso funciona se a ordem for: Ativos (60), Risco (90), Inativos (90+).
    *   *Ajuste no código acima:* Coloquei `atividade de 60 dias` e `atividade de 90 dias`. A cláusula `atividade de X dias` significa "comprou nos últimos X dias". Se um cliente comprou há 30 dias, ele tem atividade de 60 e de 90. Se a regra "Ativo" vem primeiro, ele é classificado como Ativo. Se comprou há 70 dias, não tem atividade de 60, mas tem de 90. Vai para Risco. Esta lógica está correta.
2.  **Segmento "Inativo":** O pedido diz "sem pedidos a mais de 90 dias". Usei `inatividade global de 90 dias` que é a cláusula exata para "clientes sem compra com a empresa toda há pelo menos N dias".
3.  **Segmento "Prospect":** O pedido diz "ciclo de vida prospect". Usei `no ciclo de vida prospect com a empresa` conforme o manual (seção 6.7).
4.  **Frequências:** Todas as frequências do pedido (14, 7, 28, 7) foram aplicadas exatamente como solicitado.
5.  **Ponto Falho Potencial:** A sobreposição entre "Ativo" (0-60) e "Risco" (60-90) depende estritamente da ordem das regras no arquivo. A regra "Ativo" deve vir antes de "Risco". O código acima respeita essa ordem.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativo; grupo: Ativo, Risco de inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.