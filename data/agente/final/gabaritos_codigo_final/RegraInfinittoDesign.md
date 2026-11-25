```gobr
version 1.0


time "televendas":
    vendedores todostelevendas ativados


parametros "Ativo":
    do time("televendas")
    quando atividade global de 60 dias
    frequencia de 14 dias

parametros "Risco de inatividade":
    do time("televendas")
    quando em ruptura global do trimestre
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

**Premissas assumidas:**
1.  **Ordem das regras:** Segui a ordem do pedido (Ativo, Risco, Inativo, Prospect). Como o validador GoBR aplica a primeira regra que "encaixa" e a ordem de execução é sequencial, é crucial que faixas mais restritivas ou específicas venham antes. No entanto, `inatividade global de 90 dias` (Inativo) também captura quem está em ruptura (60-90 dias) se não houver sobreposição explícita de exclusão. Os exemplos mostram que a última regra sem `quando` (ou com condição genérica) serve para "quem sobrou". Para garantir a lógica de "entre 60 e 90 dias" para Risco, a cláusula `em ruptura global do trimestre` é a mais precisa disponível no manual para esse intervalo específico.
2.  **Segmento Prospect:** O pedido pede "ciclo de vida prospect". O manual oferece `no ciclo de vida prospect com a empresa` ou `com o vendedor`. A premissa P11 diz "Prospect é sempre da empresa", então usei `prospects da empresa` (que é sinônimo funcional no contexto de filtros de inatividade/compra, ou `no ciclo de vida prospect com a empresa` se estritamente ciclo de vida). Os exemplos usam `no ciclo de vida prospect com a empresa`. Vou ajustar para usar a sintaxe exata dos exemplos para…

Pontos de atenção na modelagem:
- O pedido não diz o time (premissa P11). O arquivo usa "televendas": todos os vendedores de televendas habilitados no Govendas.