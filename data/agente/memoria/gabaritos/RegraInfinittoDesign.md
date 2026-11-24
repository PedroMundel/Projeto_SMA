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
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias
```

**Premissas e Observações:**

1.  **Ordem das Regras:** A regra "Ativo" (60 dias) vem antes de "Risco de inatividade" (90 dias) para garantir que quem comprou há 30 dias seja capturado como Ativo e não como Risco (já que 30 dias também está dentro dos 90 dias).
2.  **Critério "Entre 60 e 90 dias":** O GoBR não possui uma cláusula nativa de intervalo fechado (ex: `quando atividade entre 60 e 90 dias`). A prática padrão nos exemplos (regra_197, regra_224) para faixas intermediárias é usar o limite superior da faixa (`atividade de 90 dias`) combinada com a ordem de execução das regras (a regra de 60 dias captura os mais recentes). Assim, a regra "Risco de inatividade" com `atividade de 90 dias` atenderá quem comprou entre 61 e 90 dias, pois os de 0-60 dias já foram capturados pela regra anterior.
3.  **Segmento "Prospect":** Utilizou-se a cláusula `no ciclo de vida prospect com a empresa` conforme o manual (seção 6.7) e os exemplos.
4.  **Segmento "Inativo":** Utilizou-se `inatividade global de 90 dias` para definir clientes sem compra há mais de 90 dias.
5.  **Fidelidade:** Todos os números do pedido (60, 14, 90, 7, 28) foram mantidos exatamente como solicitados.

Pontos de atenção na modelagem:
- A cascata mistura escopos de recência de compra (global: Inativo; grupo: Ativo, Risco de inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.