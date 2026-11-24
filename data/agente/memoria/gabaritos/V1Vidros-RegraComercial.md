```gobr
version 1.0

time "todos":
    vendedores todos ativados

parametros "Clientes baixados na receita":
    do time("todos")
    quando status na receita federal definido como baixada
    nao agendar

parametros "Clientes Prospects":
    do time("todos")
    quando no ciclo de vida prospect com a empresa
    frequencia de 7 dias

parametros "Clientes Ativos":
    do time("todos")
    quando atividade de 30 dias
    frequencia de 14 dias

parametros "Risco de Inatividade":
    do time("todos")
    quando atividade de 45 dias
    frequencia de 7 dias

parametros "Inativos":
    do time("todos")
    quando inatividade global de 45 dias
    frequencia de 14 dias

parametros "Inadiplentes":
    do time("todos")
    quando inadimplentes
    frequencia de 7 dias
```

**Notas:**
1.  **Inadiplentes:** Como o usuário não respondeu à pergunta sobre a frequência e o limite de perguntas foi atingido, assumi a premissa mais comum em regras de agendamento (exemplos do manual e da base) de **7 dias** para clientes que precisam de acompanhamento ativo, como os inadimplentes autorizados. Se esta frequência estiver incorreta, ela deve ser ajustada.
2.  **Ordem das Regras:** A regra de "Inadiplentes" foi colocada ao final. Se um cliente for "Inadimplente" e também se encaixar em "Ativo" (comprou há 30 dias), a regra de "Ativo" será aplicada primeiro devido à ordem. Se a intenção for que a inadimplência prevaleça sobre o status de compra, a regra de "Inadiplentes" deve ser movida para antes das regras de "Ativo", "Risco" e "Inativos". Dado o pedido "Agendar Inadiplentes" como um segmento separado, mantive a ordem atual, mas esta é uma premissa que pode precisar de revisão.
3.  **Clientes Baixados:** Mantido como bloqueio no início, conforme padrão e pedido.

Divergências entre o pedido e as regras (conferente):
- "Inadiplentes": O pedido não especifica frequência para inadiplentes, mas a regra assume 7 dias sem confirmação; além disso, o filtro de clientes inclui critérios de compra (44 dias/45 dias) que não constam no pedido original para este segmento, apenas 'inadimplentes autorizados'. (pedido: "Agendar Inadiplentes: Clientes inadiplentes autorizados para agendamento")

Pontos de atenção na modelagem:
- Lacuna do pedido sem resposta do usuário: "Inadiplentes": de quantos em quantos dias agendar?
- A cascata mistura escopos de recência de compra (global: Inativos; grupo: Clientes Ativos, Risco de Inatividade); faixas de escopos diferentes não se excluem automaticamente e podem se sobrepor ou deixar lacunas.

Perguntas feitas:
- Para escrever as regras sem chutar, faltam estes dados no pedido:
- "Inadiplentes": de quantos em quantos dias agendar?
Responda numa mensagem só. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- Para a regra "Agendar Inadiplentes", qual deve ser a frequência de agendamento (ex: 7 dias, 14 dias)? -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.
- O pedido diz "Agendar Inadiplentes", o que implica que eles devem ser agendados (ao contrário do padrão de bloqueio visto em exemplos). Qual a frequência para estes clientes? (Ex: 7 dias, 14 dias). Além disso, confirme se deve haver uma regra específica para "Inadiplentes" ou se eles devem seguir a frequência do seu segmento de compra (Ativo, Risco, Inativo) desde que sejam autorizados. -> Sem resposta do usuário: siga com a premissa mais provável e diga nas notas qual foi.